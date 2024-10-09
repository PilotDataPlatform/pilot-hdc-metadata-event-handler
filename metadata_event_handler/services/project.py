# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any

import httpx

from metadata_event_handler.app.routers.router_exceptions import UnhandledException
from metadata_event_handler.logger import logger


class ProjectService:
    """Client to connect with project service."""

    def __init__(self, project_service_url: str) -> None:
        self.service_url = project_service_url + '/v1'

    async def get_projects(self, params: dict) -> list[dict:Any]:
        """Get info of all projects."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.service_url}/projects/', params=params)
            if response.status_code != 200:
                logger.error(f'Failed to connect to project service for project info: {response.text}')
                raise UnhandledException('Failed to connect to project service for project info')
        projects = response.json()
        return projects
