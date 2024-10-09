# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any

import pytest
from elasticsearch import AsyncElasticsearch

from metadata_event_handler.clients.elasticsearch import ElasticsearchClient


class ElasticsearchTestClient(ElasticsearchClient):
    def __init__(self) -> None:
        super().__init__(AsyncElasticsearch())

        self.documents = []

    async def insert_or_update_document(self, index: str, message: dict[str, Any]) -> None:
        self.documents.append((index, message))

    async def bulk_upsert_document(self, index: str, items: dict[str:Any]) -> None:
        self.documents.append((index, items))


@pytest.fixture
def elasticsearch_client() -> ElasticsearchTestClient:
    yield ElasticsearchTestClient()
