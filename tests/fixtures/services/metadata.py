# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest

from metadata_event_handler.config import METADATA_SERVICE
from metadata_event_handler.models.ESItemModel import ItemStatus
from metadata_event_handler.services.metadata import MetadataService


@pytest.fixture
def metadata_service() -> MetadataService:
    return MetadataService(METADATA_SERVICE)


@pytest.fixture
def get_items_response_single_page(fake, get_project_template_response):
    fake_id = str(fake.uuid4())
    template_id = get_project_template_response[0]['id']
    response = {
        'num_of_pages': 1,
        'page': 0,
        'total': 1,
        'result': [
            {
                'id': fake_id,
                'parent': None,
                'parent_path': None,
                'restore_path': None,
                'status': ItemStatus.ACTIVE,
                'type': 'name_folder',
                'zone': 0,
                'name': 'admin',
                'size': 0,
                'owner': 'admin',
                'container_code': 'kafkatest1',
                'container_type': 'project',
                'created_time': '2022-08-31 15:38:22.999269',
                'last_updated_time': '2022-08-31 15:38:22.999278',
                'storage': {'id': fake_id, 'location_uri': None, 'version': None},
                'extended': {
                    'id': fake_id,
                    'extra': {'tags': [], 'system_tags': [], 'attributes': {template_id: {'key1': 'value1'}}},
                },
            }
        ],
    }
    yield response


@pytest.fixture
def get_items_response_multi_page(fake):
    fake_id1 = str(fake.uuid4())
    fake_id2 = str(fake.uuid4())
    response = {
        'num_of_pages': 2,
        'page': 1,
        'total': 2,
        'result': [
            {
                'id': fake_id1,
                'parent': None,
                'parent_path': None,
                'restore_path': None,
                'status': ItemStatus.ACTIVE,
                'type': 'name_folder',
                'zone': 0,
                'name': 'admin',
                'size': 0,
                'owner': 'admin',
                'container_code': 'kafkatest1',
                'container_type': 'project',
                'created_time': '2022-08-31 15:38:22.999269',
                'last_updated_time': '2022-08-31 15:38:22.999278',
                'storage': {'id': fake_id1, 'location_uri': None, 'version': None},
                'extended': {
                    'id': fake_id1,
                    'extra': {'tags': [], 'system_tags': [], 'attributes': {str(fake_id1): {'key1': 'value1'}}},
                },
            },
            {
                'id': fake_id2,
                'parent': None,
                'parent_path': None,
                'restore_path': None,
                'status': ItemStatus.ACTIVE,
                'type': 'name_folder',
                'zone': 0,
                'name': 'admin',
                'size': 0,
                'owner': 'admin',
                'container_code': 'kafkatest2',
                'container_type': 'project',
                'created_time': '2022-08-31 15:38:22.999269',
                'last_updated_time': '2022-08-31 15:38:22.999278',
                'storage': {'id': fake_id2, 'location_uri': None, 'version': None},
                'extended': {
                    'id': fake_id2,
                    'extra': {'tags': [], 'system_tags': [], 'attributes': {str(fake_id2): {'key1': 'value1'}}},
                },
            },
        ],
    }
    yield response


@pytest.fixture
def get_project_template_response(fake):
    container_code = fake.pystr()
    fake_id = str(fake.uuid4())
    response = [
        {
            'id': fake_id,
            'name': 'Template01',
            'project_code': container_code,
            'attributes': [
                {'name': 'key1', 'optional': True, 'type': 'multiple_choice', 'options': ['value1', 'value2']}
            ],
        }
    ]
    yield response
