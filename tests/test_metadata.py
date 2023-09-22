# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest

from metadata_event_handler.app.routers.router_exceptions import UnhandledException
from metadata_event_handler.config import METADATA_SERVICE_PAGE_SIZE


class TestMetadataClient:
    async def test_return_template_info_for_project(self, httpx_mock, fake, metadata_service):
        container_code = fake.pystr()
        expected_response = {
            'result': [
                {
                    'id': fake.uuid4(),
                    'name': 'Template01',
                    'project_code': container_code,
                    'attributes': [
                        {'name': 'key1', 'optional': True, 'type': 'multiple_choice', 'options': ['value1', 'value2']}
                    ],
                }
            ]
        }
        httpx_mock.add_response(
            method='GET',
            url=f'{metadata_service.service_url}/template/?project_code={container_code}'
            f'&page_size={METADATA_SERVICE_PAGE_SIZE}',
            status_code=200,
            json=expected_response,
        )
        template_info = await metadata_service.get_templates(container_code=container_code)
        assert template_info == expected_response['result']

    async def test_return_no_template_info_for_project(self, httpx_mock, fake, metadata_service):
        container_code = fake.pystr()
        expected_response = {'result': []}
        httpx_mock.add_response(
            method='GET',
            url=f'{metadata_service.service_url}/template/?project_code={container_code}'
            f'&page_size={METADATA_SERVICE_PAGE_SIZE}',
            status_code=200,
            json=expected_response,
        )
        template_info = await metadata_service.get_templates(container_code=container_code)
        assert template_info == {}

    async def test_failed_to_retrieve_templates_raise_exception(self, httpx_mock, fake, metadata_service):
        container_code = fake.pystr()
        httpx_mock.add_response(
            method='GET',
            url=f'{metadata_service.service_url}/template/?project_code={container_code}'
            f'&page_size={METADATA_SERVICE_PAGE_SIZE}',
            status_code=500,
        )
        with pytest.raises(UnhandledException):
            await metadata_service.get_templates(container_code=container_code)

    async def test_return_items_from_search(self, httpx_mock, fake, metadata_service, get_items_response_single_page):
        params = {'page_size': METADATA_SERVICE_PAGE_SIZE}
        httpx_mock.add_response(
            method='GET',
            url=f'{metadata_service.service_url}/items/search/?page_size={METADATA_SERVICE_PAGE_SIZE}',
            status_code=200,
            json=get_items_response_single_page,
        )
        items = await metadata_service.get_items(params)
        assert items == get_items_response_single_page

    async def test_failed_to_retrieve_items_from_search_raise_exception(self, httpx_mock, fake, metadata_service):
        params = {'page_size': METADATA_SERVICE_PAGE_SIZE}
        httpx_mock.add_response(
            method='GET',
            url=f'{metadata_service.service_url}/items/search/?page_size={METADATA_SERVICE_PAGE_SIZE}',
            status_code=500,
        )
        with pytest.raises(UnhandledException):
            await metadata_service.get_items(params)
