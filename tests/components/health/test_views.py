# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from unittest.mock import AsyncMock


class TestHealthViews:
    async def test_health_endpoint_returns_204_when_elasticsearch_is_live(self, mocker, client):
        with mocker.patch('elasticsearch.AsyncElasticsearch.ping', new_callable=AsyncMock, return_value=True):
            response = await client.get('/v1/health/')

        assert response.status_code == 204

    async def test_health_endpoint_returns_503_when_elasticsearch_is_not_live(self, client):
        response = await client.get('/v1/health/')

        assert response.status_code == 503
