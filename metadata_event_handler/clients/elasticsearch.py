# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import logging
from typing import Any

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_scan

from metadata_event_handler.app.routers.router_exceptions import UnhandledException
from metadata_event_handler.config import ELASICSEARCH_PAGE_SIZE

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    def __init__(self, client: AsyncElasticsearch) -> None:
        self.client = client

    async def insert_or_update_document(self, index: str, message: dict[str, Any]) -> None:
        if index == 'metadata-items' or index == 'metadata-items-facet':
            identifier = {'id': message['id']} if index == 'metadata-items' else {'identifier': message['identifier']}
            search_es = await self.client.search(index=index, query={'match': identifier})
            search_hits = search_es['hits']['total']['value']
            if not search_hits:
                del message['to_delete']
                await self.client.index(index=index, body=message)
            else:
                doc_id = search_es['hits']['hits'][0]['_id']
                item_doc = search_es['hits']['hits'][0]['_source']
                if message['to_delete']:
                    await self.client.delete(index=index, id=doc_id)
                else:
                    del message['to_delete']
                    item_doc.update(message)
                    await self.client.index(index=index, body=item_doc, id=doc_id)
        else:
            await self.client.index(index=index, body=message)

    async def bulk_upsert_document(self, index: str, items: dict[str:Any]) -> None:
        """Bulk upsert items into Elasticsearch."""
        try:
            item_ids = list(items.keys())
            found_items = []
            async for doc in async_scan(
                client=self.client,
                query={'query': {'terms': {'id': item_ids}}},
                index=index,
                size=ELASICSEARCH_PAGE_SIZE,
                scroll='5m',
            ):
                found_id = doc['_source']['id']
                del items[found_id]['to_delete']
                doc['_source'].update(items[found_id])
                found_items.append({'update': {'_index': index, '_id': doc['_id']}})
                found_items.append({'doc': doc['_source']})
                del items[found_id]

            await self.client.bulk(index=index, body=found_items)
            logger.info('Successfully bulk updated items')

            if items:
                format_create = []
                for _, value in items.items():
                    format_create.append({'create': {'_index': index}})
                    format_create.append(value)
                await self.client.bulk(index=index, body=format_create)
                logger.info('Successfully bulk created items')
        except Exception:
            logger.exception('Unable to bulk index items into elasticsearch')
            raise UnhandledException()

    async def close(self):
        await self.client.close()
