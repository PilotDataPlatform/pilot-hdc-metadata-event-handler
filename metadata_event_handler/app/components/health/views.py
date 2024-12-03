# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from metadata_event_handler.app.dependencies import get_elasticsearch_client
from metadata_event_handler.clients.elasticsearch import ElasticsearchClient
from metadata_event_handler.logger import logger

router = APIRouter(prefix='/health', tags=['Health'])


@router.get('/', summary='Check the health state of the application.')
async def get_health(elasticsearch_client: ElasticsearchClient = Depends(get_elasticsearch_client)) -> Response:
    """Return response that represents status of the Elasticsearch connection."""

    logger.info('Checking if Elasticsearch is online.')

    is_online = await elasticsearch_client.client.ping()

    logger.info(f'Received is_online status "{is_online}".')

    response = Response(status_code=204)
    if not is_online:
        response = Response(status_code=503)

    return response
