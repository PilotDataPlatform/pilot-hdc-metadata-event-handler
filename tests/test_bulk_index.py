# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime

import pytest

from metadata_event_handler.app.routers.router_exceptions import ItemsNotFoundException
from metadata_event_handler.app.routers.v1.bulk_index.crud import BulkIndexItems
from tests.fixtures.clients.elasticsearch import ElasticsearchTestClient


@pytest.fixture
def elasticsearch_client() -> ElasticsearchTestClient:
    return ElasticsearchTestClient()


@pytest.fixture
def bulk(elasticsearch_client, metadata_service, project_service) -> BulkIndexItems:
    return BulkIndexItems(elasticsearch_client, metadata_service, project_service)


class TestBulkIndex:
    async def test_get_all_projects_with_no_pagination(self, mocker, bulk, get_projects_response_single_page):
        expected_response = [get_projects_response_single_page['result'][0]['code']]
        mocker.patch(
            'metadata_event_handler.services.project.ProjectService.get_projects',
            return_value=get_projects_response_single_page,
        )

        projects = await bulk.get_all_projects()
        assert projects == expected_response

    async def test_get_all_projects_with_pagination(self, mocker, bulk, get_projects_response_multi_page):
        expected_response = []
        expected_response += 3 * [get_projects_response_multi_page['result'][0]['code']]
        mocker.patch(
            'metadata_event_handler.services.project.ProjectService.get_projects',
            return_value=get_projects_response_multi_page,
        )

        projects = await bulk.get_all_projects()
        assert projects == expected_response

    async def test_get_all_templates(self, mocker, bulk, get_project_template_response):
        template = get_project_template_response[0]
        project_codes = [template['project_code']]
        expected_response = {template['id']: template}
        mocker.patch(
            'metadata_event_handler.services.metadata.MetadataService.get_templates',
            return_value=get_project_template_response,
        )

        projects = await bulk.get_all_templates(project_codes)
        assert projects == expected_response

    async def test_get_all_templates_return_no_templates_for_project(self, fake, mocker, bulk):
        project_codes = [fake.pystr()]
        expected_response = {}
        mocker.patch(
            'metadata_event_handler.services.metadata.MetadataService.get_templates',
            return_value={},
        )

        projects = await bulk.get_all_templates(project_codes)
        assert projects == expected_response

    async def test_return_items_by_date_range(self, fake, mocker, bulk, get_items_response_single_page):
        start_time = datetime.now()
        end_time = datetime.now()
        items = get_items_response_single_page['result'][0]

        expected_response = {items['id']: items}
        mocker.patch(
            'metadata_event_handler.services.metadata.MetadataService.get_items',
            return_value=get_items_response_single_page,
        )

        items = await bulk.get_items_by_date_range(start_time=start_time, end_time=end_time)

        assert items == expected_response

    async def test_return_items_by_date_range_with_pagination(self, fake, mocker, bulk, get_items_response_multi_page):
        item_1 = get_items_response_multi_page['result'][0]
        item_2 = get_items_response_multi_page['result'][1]
        expected_response = {item_1['id']: item_1, item_2['id']: item_2}
        start_time = datetime.now()
        end_time = datetime.now()

        mocker.patch(
            'metadata_event_handler.services.metadata.MetadataService.get_items',
            return_value=get_items_response_multi_page,
        )

        items = await bulk.get_items_by_date_range(start_time=start_time, end_time=end_time)
        assert items == expected_response

    async def test_return_items_by_date_range_no_items_found_raise_exception(self, fake, mocker, bulk):
        start_time = datetime.now()
        end_time = datetime.now()
        mocker.patch(
            'metadata_event_handler.services.metadata.MetadataService.get_items',
            return_value={'page': 0, 'num_of_pages': 1, 'result': []},
        )

        with pytest.raises(ItemsNotFoundException):
            await bulk.get_items_by_date_range(start_time=start_time, end_time=end_time)

    async def test_bulk_index_item(
        self,
        fake,
        mocker,
        bulk,
        get_projects_response_single_page,
        get_project_template_response,
        get_items_response_single_page,
        es_model,
        elasticsearch_client,
    ):
        start_time = datetime.now()
        end_time = datetime.now()
        mocker.patch(
            'metadata_event_handler.services.metadata.MetadataService.get_items',
            return_value=get_items_response_single_page,
        )

        mocker.patch(
            'metadata_event_handler.services.project.ProjectService.get_projects',
            return_value=get_projects_response_single_page,
        )

        mocker.patch(
            'metadata_event_handler.services.metadata.MetadataService.get_templates',
            return_value=get_project_template_response,
        )

        expected_documents = [('metadata-items', es_model)]
        await bulk.bulk_upsert(start_time=start_time, end_time=end_time)
        assert elasticsearch_client.documents == expected_documents
