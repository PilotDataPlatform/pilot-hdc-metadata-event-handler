# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import time
from io import BytesIO
from typing import Any

import pytest
from aiokafka import ConsumerRecord
from faker import Faker
from fastavro import schemaless_writer
from fastavro.schema import load_schema

from metadata_event_handler.config import KAFKA_SCHEMAS_PATH


class EventFactory:
    fake: Faker

    def __init__(self, fake: Faker) -> None:
        self.fake = fake

    def load_schema(self, name: str) -> dict[str, Any]:
        return load_schema(KAFKA_SCHEMAS_PATH / f'{name}.avsc')

    def create_binary_payload(self, topic: str, payload: dict[str, Any]) -> bytes:
        buffer = BytesIO()
        schemaless_writer(buffer, self.load_schema(topic), payload)
        return buffer.getvalue()

    def generate_event(self, topic: str, key: Any, value: Any) -> ConsumerRecord:
        return ConsumerRecord(
            topic=topic,
            key=key,
            value=value,
            partition=self.fake.pyint(),
            offset=self.fake.pyint(),
            timestamp=int(time.time() * 1000),
            timestamp_type=0,
            headers=[],
            checksum=0,
            serialized_key_size=self.fake.pyint(),
            serialized_value_size=self.fake.pyint(),
        )

    def generate_metadata_item_event_v1(self, payload: dict[str, Any]) -> ConsumerRecord:
        topic = 'metadata.items'

        value = self.create_binary_payload(topic, payload)

        return self.generate_event(topic=topic, key=None, value=value)

    def generate_item_activity_event_v1(self, payload: dict[str, Any]) -> ConsumerRecord:
        topic = 'metadata.items.activity'

        value = self.create_binary_payload(topic, payload)

        return self.generate_event(topic=topic, key=None, value=value)

    def generate_dataset_activity_event_v1(self, payload: dict[str, Any]) -> ConsumerRecord:
        topic = 'dataset.activity'

        value = self.create_binary_payload(topic, payload)

        return self.generate_event(topic=topic, key=None, value=value)


@pytest.fixture
def event_factory(fake) -> EventFactory:
    yield EventFactory(fake)
