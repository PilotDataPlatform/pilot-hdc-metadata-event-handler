# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from elasticsearch import AsyncElasticsearch

from metadata_event_handler.clients.elasticsearch import ElasticsearchClient
from metadata_event_handler.config import ELASTICSEARCH_SERVICE


async def get_elasticsearch_client() -> ElasticsearchClient:
    """Create a callable dependency for Elasticsearch client instance."""

    client = ElasticsearchClient(AsyncElasticsearch(ELASTICSEARCH_SERVICE))

    try:
        yield client
    finally:
        await client.close()
