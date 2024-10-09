# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import base64
import io
import logging
import math
from datetime import datetime
from typing import Any

from aiokafka import ConsumerRecord
from fastavro import schema
from fastavro import schemaless_reader
from fastavro import validate

logger = logging.getLogger(__name__)


class BaseConsumer:
    def __init__(self) -> None:
        pass

    def decode_label_from_ltree(self, encoded_string: str) -> str:
        missing_padding = math.ceil(len(encoded_string) / 8) * 8 - len(encoded_string)
        if missing_padding:
            encoded_string += '=' * missing_padding
        utf8_string = base64.b32decode(encoded_string.encode('utf-8')).decode('utf-8')
        return utf8_string

    def convert_timestamp_millis_to_second(self, timestamp: int) -> int:
        return timestamp // 1000

    def convert_datetime_to_timestamp(self, date: datetime) -> int:
        return int(date.timestamp())

    def decode_message(self, message: bytes, topic: str) -> dict[str, Any]:
        logger.info(f'Starting to decode message from topic "{topic}".')
        try:
            imported_schema = schema.load_schema(self.KAFKA_SCHEMAS_PATH / f'{topic}.avsc')
            message_reader = io.BytesIO(message)
            message_decoded = schemaless_reader(message_reader, imported_schema)
            is_valid = validate(message_decoded, imported_schema, raise_errors=False)
            logger.info(f'Decoded a message from a topic "{topic}": {message_decoded}')
            if not is_valid:
                logger.warning(f'Unable validate decoded message from topic "{topic}".')
                return {}

        except Exception:
            logger.exception(f'Unable to decode message from topic "{topic}".')
            return {}

        logger.info(f'Decoded a message from a topic "{topic}": {message_decoded}')
        return message_decoded

    async def process_event(self, event: ConsumerRecord) -> None:
        topic = event.topic
        message = self.decode_message(message=event.value, topic=topic)
        if not message:
            await self.producer.send_and_wait('metadata.dlq', event.value)
        else:
            await self.process_topic_message(topic, message)

    async def process_topic_message(self, topic: str, message: dict[str, Any]) -> None:
        pass

    async def run(self) -> None:
        raise Exception('The class is missing the entry funtion `run()`!')
