# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from unittest.mock import patch

from elasticsearch import AsyncElasticsearch

from metadata_event_handler.clients.elasticsearch import ElasticsearchClient


class TestElasticsearchClient:
    async def test_insert_or_update_item_document(self, mocker):
        class FakeES(AsyncElasticsearch):
            async def search(self, index, query):
                return {
                    'hits': {
                        'total': {'value': 0},
                        'hits': [],
                    }
                }

            async def index(self, index, body, id=None):  # noqa F401
                return {
                    'hits': {
                        'total': {'value': 1},
                        'hits': [
                            {
                                '_id': '123',
                                '_source': {
                                    'id': '123',
                                    'name': 'test1',
                                    'to_delete': False,
                                },
                            }
                        ],
                    }
                }

        es_client = ElasticsearchClient(FakeES())
        with patch.object(FakeES, 'search') as mock:
            await es_client.insert_or_update_document(
                index='metadata-items', message={'id': 'items_id', 'to_delete': False}
            )
            assert mock.call_count == 1
            mock.assert_called_with(index='metadata-items', query={'match': {'id': 'items_id'}})

            await es_client.insert_or_update_document(
                index='metadata-items-facet', message={'identifier': 'facet_idnetifier', 'to_delete': False}
            )
            assert mock.call_count == 2
            mock.assert_called_with(index='metadata-items-facet', query={'match': {'identifier': 'facet_idnetifier'}})

            await es_client.insert_or_update_document(
                index='metadata-items-activity', message={'id': 'activity_id', 'to_delete': False}
            )
            assert mock.call_count == 2
