# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest

from metadata_event_handler.config import PROJECT_SERVICE
from metadata_event_handler.services.project import ProjectService


@pytest.fixture
def project_service() -> ProjectService:
    return ProjectService(PROJECT_SERVICE)


@pytest.fixture
def get_projects_response_multi_page(fake):
    fake_id = str(fake.uuid4())
    container_code = fake.pystr()
    response = {
        'num_of_pages': 2,
        'page': 1,
        'total': 1,
        'result': [
            {
                'code': container_code,
                'name': 'test project2',
                'description': 'test project2',
                'logo_name': '',
                'tags': [],
                'system_tags': [],
                'is_discoverable': True,
                'id': fake_id,
                'created_at': '2022-07-26T18:16:03.820708+00:00',
                'image_url': '',
            }
        ],
    }
    yield response


@pytest.fixture
def get_projects_response_single_page(fake):
    fake_id = str(fake.uuid4())
    container_code = fake.pystr()
    response = {
        'num_of_pages': 1,
        'page': 0,
        'total': 1,
        'result': [
            {
                'code': container_code,
                'name': 'test project',
                'description': 'test project',
                'logo_name': '',
                'tags': [],
                'system_tags': [],
                'is_discoverable': True,
                'id': fake_id,
                'created_at': '2022-07-26T18:16:03.820708+00:00',
                'image_url': '',
            }
        ],
    }
    yield response
