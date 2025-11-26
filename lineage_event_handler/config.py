# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import logging
from pathlib import Path

from pydantic import BaseSettings
from pydantic import Extra


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'lineage_consumer'
    VERSION: str = '1.0.7'
    LOGGING_LEVEL: int = logging.INFO
    LOGGING_FORMAT: str = 'json'

    ATLAS_API: str
    ATLAS_ENTITY_TYPE: str
    ATLAS_ADMIN: str
    ATLAS_PASSWD: str
    ATLAS_ENTITY_DIR = Path(__file__).parent / 'atlas_entity'

    KAFKA_SERVICE: str
    KAFKA_TOPICS: list[str]
    KAFKA_GROUP_ID: str

    KAFKA_SCHEMAS_PATH = Path(__file__).parent / 'kafka_schemas'
    ELASTICSEARCH_SERVICE: str

    SEEK_TO_BEGINNING: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow


ConfigClass = Settings()
