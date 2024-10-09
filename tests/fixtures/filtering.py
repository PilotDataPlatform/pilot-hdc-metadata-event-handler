# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime

import pytest

from commons.encoders import convert_datetime_to_timestamp_millisecond
from metadata_event_handler.models.ESItemModel import ItemStatus


@pytest.fixture
def item_message(fake):
    item = {
        'id': fake.uuid4(),
        'parent': fake.uuid4(),
        'parent_path': 'admin',
        'restore_path': None,
        'status': ItemStatus.ACTIVE,
        'type': 'file',
        'zone': 0,
        'name': fake.name(),
        'size': 1565,
        'owner': 'admin',
        'container_code': fake.name(),
        'container_type': 'project',
        'created_time': datetime.now(),
        'last_updated_time': datetime.now(),
        'to_delete': False,
        'storage': {'id': fake.uuid4(), 'location_uri': '', 'version': ''},
        'extended': {
            'id': fake.uuid4(),
            'template_name': fake.name(),
            'extra': {'tags': [], 'system_tags': [], 'attributes': {}},
        },
    }
    yield item


@pytest.fixture
def filtered_item(item_message):
    yield {
        'container_code': item_message['container_code'],
        'created_time': convert_datetime_to_timestamp_millisecond(item_message['created_time']),
        'identifier': item_message['id'],
        'last_updated_time': convert_datetime_to_timestamp_millisecond(item_message['last_updated_time']),
        'name': item_message['name'],
        'owner': item_message['owner'],
        'parent_path': item_message['parent_path'],
        'size': item_message['size'],
        'system_tags': item_message['extended']['extra']['system_tags'],
        'tags': item_message['extended']['extra']['tags'],
        'template_name': item_message['extended']['template_name'],
        'type': item_message['type'],
        'zone': 'greenroom' if item_message['zone'] == 0 else 'core',
        'zonefilter': 'greenroom' if item_message['zone'] == 0 else 'core',
        'to_delete': False,
    }
