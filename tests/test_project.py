# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest

from metadata_event_handler.app.routers.router_exceptions import UnhandledException
from metadata_event_handler.config import PROJECT_SERVICE_PAGE_SIZE


class TestProjectClient:
    async def test_return_projects(self, httpx_mock, project_service, get_projects_response_single_page):
        params = {'page_size': PROJECT_SERVICE_PAGE_SIZE}
        httpx_mock.add_response(
            method='GET',
            url=project_service.service_url + f'/projects/?page_size={PROJECT_SERVICE_PAGE_SIZE}',
            json=get_projects_response_single_page,
        )

        projects = await project_service.get_projects(params)
        assert projects == get_projects_response_single_page

    async def test_return_projects_failed_to_retrieve_projects_raise_exception(
        self, httpx_mock, project_service, get_projects_response_single_page
    ):
        params = {'page_size': PROJECT_SERVICE_PAGE_SIZE}
        httpx_mock.add_response(
            method='GET',
            url=project_service.service_url + f'/projects/?page_size={PROJECT_SERVICE_PAGE_SIZE}',
            status_code=500,
        )

        with pytest.raises(UnhandledException):
            await project_service.get_projects(params)
