# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any
from typing import Union

from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
from elasticsearch import AsyncElasticsearch

from commons.base_consumer import BaseConsumer
from metadata_event_handler.clients.elasticsearch import ElasticsearchClient
from metadata_event_handler.config import CONSUMER_GROUP
from metadata_event_handler.config import ELASTICSEARCH_SERVICE
from metadata_event_handler.config import KAFKA_SCHEMAS_PATH
from metadata_event_handler.config import KAFKA_SERVICE
from metadata_event_handler.config import KAFKA_TOPICS
from metadata_event_handler.config import SEEK_TO_BEGINNING
from metadata_event_handler.logger import logger
from metadata_event_handler.models import ESDatasetActivityModel
from metadata_event_handler.models import ESItemActivityModel
from metadata_event_handler.models import ESItemModel

es_index = {
    ESItemModel: 'metadata-items',
    ESItemActivityModel: 'items-activity-logs',
    ESDatasetActivityModel: 'datasets-activity-logs',
}


class MetadataConsumer(BaseConsumer):
    def __init__(self, es_client: ElasticsearchClient | None = None) -> None:
        if es_client is None:
            es_client = ElasticsearchClient(AsyncElasticsearch(ELASTICSEARCH_SERVICE))
        self.es_client = es_client
        self.KAFKA_SCHEMAS_PATH = KAFKA_SCHEMAS_PATH

        self.pending_items = {}
        self.consumer = None
        self.producer = None

    async def write_to_elasticsearch(
        self, es_doc: Union[ESItemModel, ESItemActivityModel, ESDatasetActivityModel]
    ) -> None:
        logger.info('Writing to elasticsearch')
        doc = es_doc.to_dict()
        index = es_index[type(es_doc)]
        await self.es_client.insert_or_update_document(index=index, message=doc)

    async def parse_items_message(self, message: dict[str, Any]) -> None:
        item_id = message['id']
        logger.info(f'Consumed items event ({item_id})')
        es_item = ESItemModel()
        es_item.id = item_id
        es_item.parent = message['parent']
        es_item.parent_path = message['parent_path']
        es_item.restore_path = message['restore_path']
        es_item.status = message['status']
        es_item.type = message['type']
        es_item.zone = message['zone']
        es_item.name = message['name']
        es_item.size = message['size']
        es_item.owner = message['owner']
        es_item.container_code = message['container_code']
        es_item.container_type = message['container_type']
        es_item.created_time = self.convert_datetime_to_timestamp(message['created_time'])
        es_item.last_updated_time = self.convert_datetime_to_timestamp(message['last_updated_time'])
        es_item.to_delete = message['to_delete']
        item_storage = message['storage']
        es_item.storage_id = item_storage['id']
        es_item.location_uri = item_storage['location_uri']
        es_item.version = item_storage['version']
        item_extended = message['extended']
        es_item.extended_id = item_extended['id']
        es_item.template_id = item_extended['template_id']
        es_item.template_name = item_extended['template_name']
        es_item.tags = item_extended['extra']['tags']
        es_item.system_tags = item_extended['extra']['system_tags']
        es_item.attributes = (
            item_extended['extra']['attributes'][str(es_item.template_id)]
            if item_extended['extra']['attributes']
            else {}
        )
        await self.write_to_elasticsearch(es_item)

    async def parse_item_activity_message(self, message: dict[str, Any]) -> None:
        item_id = message['item_id']
        logger.info(f'Consumed activity event ({item_id})')
        es_item = ESItemActivityModel()
        es_item.activity_type = message['activity_type']
        es_item.activity_time = self.convert_datetime_to_timestamp(message['activity_time'])
        es_item.item_id = message['item_id']
        es_item.item_type = message['item_type']
        es_item.item_name = message['item_name']
        es_item.item_parent_path = message['item_parent_path']
        es_item.container_code = message['container_code']
        es_item.container_type = message['container_type']
        es_item.zone = message['zone']
        es_item.user = message['user']
        es_item.imported_from = message['imported_from']
        es_item.changes = message['changes']
        await self.write_to_elasticsearch(es_item)

    async def parse_dataset_activity_message(self, message: dict[str, Any]) -> None:
        es_dataset = ESDatasetActivityModel()
        es_dataset.activity_type = message['activity_type']
        es_dataset.activity_time = self.convert_datetime_to_timestamp(message['activity_time'])
        es_dataset.container_code = message['container_code']
        es_dataset.target_name = message['target_name']
        es_dataset.version = message['version']
        es_dataset.user = message['user']
        es_dataset.changes = message['changes']
        await self.write_to_elasticsearch(es_dataset)

    async def process_topic_message(self, topic: str, message: dict[str, Any]) -> None:
        if topic == 'metadata.items':
            await self.parse_items_message(message)
        elif topic == 'metadata.items.activity':
            await self.parse_item_activity_message(message)
        elif topic == 'dataset.activity':
            await self.parse_dataset_activity_message(message)

    async def run(self) -> None:
        logger.info('Running consumer')
        self.consumer = AIOKafkaConsumer(bootstrap_servers=[KAFKA_SERVICE], group_id=CONSUMER_GROUP)
        self.consumer.subscribe(KAFKA_TOPICS)
        self.producer = AIOKafkaProducer(bootstrap_servers=[KAFKA_SERVICE])
        await self.consumer.start()
        if SEEK_TO_BEGINNING:
            await self.consumer.seek_to_beginning()
        await self.producer.start()
        try:
            async for event in self.consumer:
                logger.info(f'Received an event from topic "{event.topic}".')
                try:
                    await self.process_event(event)
                except Exception:
                    logger.exception(
                        f'Unable to process an event from topic "{event.topic}", '
                        f'partition "{event.partition}, offset "{event.offset}".'
                    )
        finally:
            logger.info('Stopping consumer')
            await self.consumer.stop()
            await self.producer.stop()
            await self.es_client.close()
