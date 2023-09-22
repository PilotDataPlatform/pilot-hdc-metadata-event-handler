# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import logging
from datetime import datetime
from typing import Any

from metadata_event_handler.app.routers.router_exceptions import ItemsNotFoundException
from metadata_event_handler.app.routers.v1.bulk_index.utils import get_items_model
from metadata_event_handler.clients.elasticsearch import ElasticsearchClient
from metadata_event_handler.config import METADATA_SERVICE_PAGE_SIZE
from metadata_event_handler.config import PROJECT_SERVICE_PAGE_SIZE
from metadata_event_handler.models.ESItemModel import ItemStatus
from metadata_event_handler.services.metadata import MetadataService
from metadata_event_handler.services.project import ProjectService

logger = logging.getLogger(__name__)


class BulkIndexItems:
    """Bulk managing documents in metadata-items index."""

    def __init__(
        self, es_client: ElasticsearchClient, metadata_client: MetadataService, project_client: ProjectService
    ):
        self.es_client = es_client
        self.metadata_client = metadata_client
        self.project_client = project_client

    async def get_all_projects(self) -> list[str]:
        """Get all projects from project service."""
        project_codes = []
        params = {'page_size': PROJECT_SERVICE_PAGE_SIZE}
        projects = await self.project_client.get_projects(params=params)
        for project in projects['result']:
            project_codes.append(project['code'])
        total_pages = int(projects['num_of_pages'])
        if total_pages > 1:
            for page in range(1, total_pages + 1):
                params['page'] = page
                project_page = await self.project_client.get_projects(params)
                project_result = project_page['result']
                for project in project_result:
                    project_codes.append(project['code'])
        return project_codes

    async def get_all_templates(self, projects: list) -> dict[str:Any]:
        """Get all templates associated with an items project and assign to item."""
        template_info = {}
        for project in projects:
            project_template = await self.metadata_client.get_templates(project)
            if project_template:
                for template in project_template:
                    template_info[template['id']] = template
        return template_info

    async def get_items_by_date_range(self, start_time: datetime, end_time: datetime) -> dict[str, Any]:
        """Search for all items by date-range recursively."""
        project_items = {}
        status = [ItemStatus.ACTIVE, ItemStatus.REGISTERED, ItemStatus.ARCHIVED]
        for archive_state in status:
            params = {
                'last_updated_start': start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'last_updated_end': end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'recursive': True,
                'status': archive_state,
                'page_size': METADATA_SERVICE_PAGE_SIZE,
            }
            items = await self.metadata_client.get_items(params)
            for item in items['result']:
                project_items[item['id']] = item
            total_pages = int(items['num_of_pages'])
            if total_pages > 1:
                for page in range(1, total_pages + 1):
                    params['page'] = page
                    items_page = await self.metadata_client.get_items(params)
                    items_result = items_page['result']
                    for item in items_result:
                        project_items[item['id']] = item
        if not project_items:
            raise ItemsNotFoundException()
        return project_items

    def get_es_models(self, items: dict[str, Any], templates: dict[str, Any]) -> dict[str:Any]:
        """Translate items into Elasticsearch model for indexing."""
        item_models = get_items_model(items=items, template_info=templates)
        return item_models

    async def bulk_upsert(self, start_time: datetime, end_time: datetime) -> None:
        """Execute bulk upsert of items between date-range into Elasticsearch."""
        items_found = await self.get_items_by_date_range(start_time=start_time, end_time=end_time)
        logger.info('Received metadata items from date-range')
        projects = await self.get_all_projects()
        templates = await self.get_all_templates(projects=projects)
        logger.info('Retrieved template info across projects')
        item_model = self.get_es_models(items=items_found, templates=templates)
        logger.info('Items successfully translated to ES model')
        await self.es_client.bulk_upsert_document(index='metadata-items', items=item_model)
        logger.info('Successfully executed elasticsearch upsert')
