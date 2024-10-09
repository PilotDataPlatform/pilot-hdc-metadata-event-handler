# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest

from metadata_event_handler.app.routers.v1.bulk_index.utils import convert_date_to_timestamp


@pytest.fixture
def parse_item_response(get_items_response_single_page):
    item = get_items_response_single_page['result'][0]
    response = {
        'id': item['id'],
        'parent': item['parent'],
        'parent_path': item['parent_path'],
        'restore_path': item['restore_path'],
        'status': item['status'],
        'type': item['type'],
        'zone': item['zone'],
        'name': item['name'],
        'size': item['size'],
        'owner': item['owner'],
        'container_code': item['container_code'],
        'container_type': item['container_type'],
        'created_time': convert_date_to_timestamp(item['created_time']),
        'last_updated_time': convert_date_to_timestamp(item['last_updated_time']),
        'storage_id': item['storage']['id'],
        'location_uri': item['storage']['location_uri'],
        'version': item['storage']['version'],
        'extended_id': item['extended']['id'],
        'tags': item['extended']['extra']['tags'],
        'to_delete': False,
        'system_tags': item['extended']['extra']['system_tags'],
        'attributes': item['extended']['extra']['attributes'],
    }
    yield response


@pytest.fixture
def es_model(get_items_response_single_page, get_project_template_response):
    item = get_items_response_single_page['result'][0]
    template = get_project_template_response[0]
    template_id = template['id']
    response = {
        item['id']: {
            'id': item['id'],
            'parent': item['parent'],
            'parent_path': item['parent_path'],
            'restore_path': item['restore_path'],
            'status': item['status'],
            'type': item['type'],
            'zone': item['zone'],
            'name': item['name'],
            'size': item['size'],
            'owner': item['owner'],
            'container_code': item['container_code'],
            'container_type': item['container_type'],
            'created_time': convert_date_to_timestamp(item['created_time']),
            'last_updated_time': convert_date_to_timestamp(item['last_updated_time']),
            'storage_id': item['storage']['id'],
            'location_uri': item['storage']['location_uri'],
            'version': item['storage']['version'],
            'extended_id': item['extended']['id'],
            'tags': item['extended']['extra']['tags'],
            'system_tags': item['extended']['extra']['system_tags'],
            'template_name': template['name'],
            'to_delete': False,
            'template_id': template_id,
            'attributes': item['extended']['extra']['attributes'][template_id],
        }
    }
    yield response
