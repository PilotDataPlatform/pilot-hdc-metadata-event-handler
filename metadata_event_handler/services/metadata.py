# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any

import httpx

from metadata_event_handler.app.routers.router_exceptions import UnhandledException
from metadata_event_handler.logger import logger


class MetadataService:
    """Client to connect with metadata service."""

    def __init__(self, metadata_service_url: str) -> None:
        self.service_url = metadata_service_url + '/v1'

    async def get_templates(self, container_code: str) -> list[dict:Any] | dict:
        """Get templates within a given project."""
        async with httpx.AsyncClient() as client:
            params = {'project_code': container_code, 'page_size': 50}
            response = await client.get(f'{self.service_url}/template/', params=params)
            if response.status_code != 200:
                logger.error(f'Failed to connect to metadata service for template info: {response.text}')
                raise UnhandledException('Failed to connect to metadata service for template info')
        template_info = response.json()['result']
        if not template_info:
            return {}
        return template_info

    async def get_items(self, params: dict) -> dict[str, Any] | None:
        """Search for items with respective characteristics."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.service_url}/items/search/', params=params)
        if response.status_code != 200:
            logger.error(f'Failed to connect to metadata service for item searching: {response.text}')
            raise UnhandledException('Failed to connect to metadata service for item searching')
        items = response.json()
        return items
