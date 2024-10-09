# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
from typing import Any

import httpx
from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
from common import LineageClient

from commons.base_consumer import BaseConsumer
from lineage_event_handler.config import ConfigClass
from lineage_event_handler.logger import logger


class LineageConsumer(BaseConsumer):
    def __init__(self) -> None:
        self.lineage_client = LineageClient(ConfigClass.ATLAS_API, ConfigClass.ATLAS_ADMIN, ConfigClass.ATLAS_PASSWD)

        self.pending_items = {}
        self.consumer = None
        self.producer = None
        self.KAFKA_SCHEMAS_PATH = ConfigClass.KAFKA_SCHEMAS_PATH

        self._check_atlas_entity_type()

    def _check_atlas_entity_type(self):
        with httpx.Client(verify=False) as client:
            response = client.get(
                ConfigClass.ATLAS_API + f'/api/atlas/v2/types/entitydef/name/{ConfigClass.ATLAS_ENTITY_TYPE}',
                auth=(ConfigClass.ATLAS_ADMIN, ConfigClass.ATLAS_PASSWD),
                timeout=60,
            )

            if response.status_code == 404:
                logger.warning(f"Entity {ConfigClass.ATLAS_ENTITY_TYPE} doesn't exist. Creating a new type.")
                entity_def_file = open(ConfigClass.ATLAS_ENTITY_DIR / f'{ConfigClass.ATLAS_ENTITY_TYPE}.json', 'r')
                entity_def = json.loads(entity_def_file.read())

                response = client.post(
                    ConfigClass.ATLAS_API + '/api/atlas/v2/types/typedefs',
                    json=entity_def,
                    auth=(ConfigClass.ATLAS_ADMIN, ConfigClass.ATLAS_PASSWD),
                    timeout=60,
                )

            elif response.status_code != 200:
                error_msg = f'Fail to get entity {ConfigClass.ATLAS_ENTITY_TYPE}'
                logger.error(error_msg)
                raise Exception(error_msg)

    async def process_item_activity_message(self, message: dict):
        """
        Summary:
            The function will is to handle lineage create in atlas.
            The new entity will only apply for file item

        Parameter:
            - message(dict): the message from item activity

        return:
            - None
        """

        action_type = message.get('activity_type')
        item_id = str(message.get('item_id'))
        logger.info(f'Processing on activity {action_type} {item_id}')

        if action_type == 'copy':
            old_path, new_path = None, None
            old_id, new_id = None, None

            for x in message.get('changes'):
                if x.get('item_property') == 'path':
                    old_path, new_path = x.get('old_value'), x.get('new_value')
                elif x.get('item_property') == 'id':
                    old_id, new_id = x.get('old_value'), x.get('new_value')

            new_parent_path, new_file_name = new_path.rsplit('/', 1)

            await self.lineage_client.update_entity(
                new_id,
                new_file_name,
                new_parent_path,
                message.get('container_code'),
                message.get('user'),
                1,
                ConfigClass.ATLAS_ENTITY_TYPE,
                container_type=message.get('container_type'),
                archive=message.get('archived', False),
            )
            logger.info(f'create entity infomation for {new_id}')

            await self.lineage_client.create_lineage(
                old_id,
                new_id,
                old_path,
                new_path,
                message.get('container_code'),
                action_type,
                ConfigClass.ATLAS_ENTITY_TYPE,
            )

            logger.info(f'create lineage infomation between {old_id} and {new_id}')

        elif action_type == 'upload' or action_type == 'delete':
            new_id = str(message.get('item_id'))
            archive = action_type == 'delete'

            await self.lineage_client.update_entity(
                new_id,
                message.get('item_name'),
                message.get('item_parent_path'),
                message.get('container_code'),
                message.get('user'),
                message.get('zone'),
                ConfigClass.ATLAS_ENTITY_TYPE,
                container_type=message.get('container_type'),
                archive=archive,
            )
            logger.info(f'create entity infomation for {new_id}')
        else:
            logger.warning(f'Type {action_type} will not create lineage in atlas')

    async def process_topic_message(self, topic: str, message: dict[str, Any]) -> None:
        if topic == 'metadata.items.activity':
            await self.process_item_activity_message(message)

    async def run(self) -> None:
        logger.info('Running LineageConsumer consumer')
        self.consumer = AIOKafkaConsumer(
            bootstrap_servers=[ConfigClass.KAFKA_SERVICE], group_id=ConfigClass.KAFKA_GROUP_ID
        )
        self.consumer.subscribe(ConfigClass.KAFKA_TOPICS)
        self.producer = AIOKafkaProducer(bootstrap_servers=[ConfigClass.KAFKA_SERVICE])
        await self.consumer.start()
        if ConfigClass.SEEK_TO_BEGINNING:
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
