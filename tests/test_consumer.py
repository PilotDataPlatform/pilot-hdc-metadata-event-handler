# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import timezone
from uuid import UUID

import pytest

from metadata_event_handler.consumer import MetadataConsumer
from metadata_event_handler.filtering import MetadataItemFacetFiltering
from metadata_event_handler.models import ESDatasetActivityModel
from metadata_event_handler.models import ESItemActivityModel
from metadata_event_handler.models import ESItemModel
from metadata_event_handler.models.ESItemModel import ItemStatus


@pytest.fixture
def metadata_consumer(elasticsearch_client) -> MetadataConsumer:
    yield MetadataConsumer(elasticsearch_client)


class TestMetadataConsumer:
    async def test_process_event_parses_metadata_item_event_structure_and_writes_into_elasticsearch(
        self, elasticsearch_client, metadata_consumer, event_factory, fake
    ):
        item_pk = fake.uuid4(cast_to=None)
        extended_pk = fake.uuid4(cast_to=None)
        storage_pk = fake.uuid4(cast_to=None)
        template_pk = fake.uuid4(cast_to=None)
        created_time = fake.postgres_timestamp()
        last_updated_time = fake.postgres_timestamp()
        metadata_item_event_payload = {
            'id': item_pk,
            'parent': fake.uuid4(cast_to=None),
            'parent_path': 'parent.path',
            'restore_path': None,
            'status': ItemStatus.ACTIVE,
            'type': 'file',
            'zone': 0,
            'name': 'file123.zip',
            'size': 2535384,
            'owner': 'amyguindoc14',
            'container_code': 'newtest0720',
            'container_type': 'project',
            'created_time': created_time,
            'last_updated_time': last_updated_time,
            'to_delete': False,
            'storage': {'id': storage_pk, 'location_uri': 'testlocation', 'version': None},
            'extended': {
                'id': extended_pk,
                'template_name': 'biomarker',
                'template_id': template_pk,
                'extra': {
                    'tags': ['new_tag'],
                    'system_tags': [],
                    'attributes': {str(template_pk): {'key1': 'value1', 'key2': 'value2'}},
                },
            },
        }
        metadata_item_event = event_factory.generate_metadata_item_event_v1(metadata_item_event_payload)
        await metadata_consumer.process_event(metadata_item_event)
        expected_metadata_item = ESItemModel()
        expected_metadata_item.id = item_pk
        expected_metadata_item.parent = metadata_item_event_payload['parent']
        expected_metadata_item.parent_path = metadata_item_event_payload['parent_path']
        expected_metadata_item.restore_path = metadata_item_event_payload['restore_path']
        expected_metadata_item.status = metadata_item_event_payload['status']
        expected_metadata_item.type = metadata_item_event_payload['type']
        expected_metadata_item.zone = metadata_item_event_payload['zone']
        expected_metadata_item.name = metadata_item_event_payload['name']
        expected_metadata_item.size = metadata_item_event_payload['size']
        expected_metadata_item.owner = metadata_item_event_payload['owner']
        expected_metadata_item.container_code = metadata_item_event_payload['container_code']
        expected_metadata_item.container_type = metadata_item_event_payload['container_type']
        expected_metadata_item.created_time = metadata_consumer.convert_datetime_to_timestamp(
            metadata_item_event_payload['created_time']
        )
        expected_metadata_item.last_updated_time = metadata_consumer.convert_datetime_to_timestamp(
            metadata_item_event_payload['last_updated_time']
        )
        expected_metadata_item.to_delete = metadata_item_event_payload['to_delete']
        expected_metadata_item.storage_id = storage_pk
        expected_metadata_item.location_uri = metadata_item_event_payload['storage']['location_uri']
        expected_metadata_item.version = metadata_item_event_payload['storage']['version']
        expected_metadata_item.extended_id = extended_pk
        expected_metadata_item.template_id = template_pk
        expected_metadata_item.template_name = metadata_item_event_payload['extended']['template_name']
        expected_metadata_item.tags = metadata_item_event_payload['extended']['extra']['tags']
        expected_metadata_item.system_tags = metadata_item_event_payload['extended']['extra']['system_tags']
        expected_metadata_item.attributes = metadata_item_event_payload['extended']['extra']['attributes'][
            str(template_pk)
        ]
        filtered_metadata = MetadataItemFacetFiltering(metadata_item_event_payload)
        expected_filtered_metadata_item = [('metadata-items-facet', filtered_metadata.apply().to_dict())]
        expected_documents = [('metadata-items', expected_metadata_item.to_dict())]
        assert elasticsearch_client.documents[0] == expected_documents[0]
        assert elasticsearch_client.documents[1] == expected_filtered_metadata_item[0]

    async def test_process_event_parses_item_activity_event_structure_and_writes_into_elasticsearch(
        self, elasticsearch_client, metadata_consumer, event_factory, fake
    ):
        item_activity_event_payload = {
            'item_id': fake.uuid4(),
            'item_name': 'Afile',
            'item_type': 'file',
            'item_parent_path': 'jzhang7.folder1',
            'container_code': 'newtest0720',
            'container_type': 'project',
            'zone': 0,
            'user': 'jzhang7',
            'imported_from': '',
            'activity_type': 'upload',
            'activity_time': datetime.now(tz=timezone.utc).replace(microsecond=0),
            'changes': [],
        }
        item_activity_event = event_factory.generate_item_activity_event_v1(item_activity_event_payload)
        await metadata_consumer.process_event(item_activity_event)

        expected_item_activity = ESItemActivityModel()
        expected_item_activity.activity_type = item_activity_event_payload['activity_type']
        expected_item_activity.activity_time = metadata_consumer.convert_datetime_to_timestamp(
            item_activity_event_payload['activity_time']
        )
        expected_item_activity.item_id = UUID(item_activity_event_payload['item_id'])
        expected_item_activity.item_type = item_activity_event_payload['item_type']
        expected_item_activity.item_name = item_activity_event_payload['item_name']
        expected_item_activity.item_parent_path = item_activity_event_payload['item_parent_path']
        expected_item_activity.container_code = item_activity_event_payload['container_code']
        expected_item_activity.container_type = item_activity_event_payload['container_type']
        expected_item_activity.zone = item_activity_event_payload['zone']
        expected_item_activity.user = item_activity_event_payload['user']
        expected_item_activity.imported_from = item_activity_event_payload['imported_from']
        expected_item_activity.changes = item_activity_event_payload['changes']

        expected_documents = [('items-activity-logs', expected_item_activity.to_dict())]

        assert elasticsearch_client.documents == expected_documents

    async def test_process_event_parses_dataset_activity_event_structure_and_writes_into_elasticsearch(
        self, elasticsearch_client, metadata_consumer, event_factory
    ):
        dataset_activity_event_payload = {
            'container_code': 'anthtest22',
            'version': None,
            'user': 'admin',
            'target_name': '/data/vre-storage/tmp/datasetanthtest22_1658430106.5204058.zip',
            'activity_type': 'download',
            'activity_time': datetime.now(tz=timezone.utc).replace(microsecond=0),
            'changes': [],
        }
        dataset_activity_event = event_factory.generate_dataset_activity_event_v1(dataset_activity_event_payload)
        await metadata_consumer.process_event(dataset_activity_event)

        expected_dataset_activity = ESDatasetActivityModel()
        expected_dataset_activity.activity_type = dataset_activity_event_payload['activity_type']
        expected_dataset_activity.activity_time = metadata_consumer.convert_datetime_to_timestamp(
            dataset_activity_event_payload['activity_time']
        )
        expected_dataset_activity.container_code = dataset_activity_event_payload['container_code']
        expected_dataset_activity.user = dataset_activity_event_payload['user']
        expected_dataset_activity.target_name = dataset_activity_event_payload['target_name']
        expected_dataset_activity.version = dataset_activity_event_payload['version']
        expected_dataset_activity.changes = dataset_activity_event_payload['changes']

        expected_documents = [('datasets-activity-logs', expected_dataset_activity.to_dict())]

        assert elasticsearch_client.documents == expected_documents
