# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import os
from pathlib import Path
from typing import Any
from typing import Dict

from common import VaultClient
from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic import Extra

load_dotenv('.env')

SRV_NAMESPACE = os.getenv('APP_NAME', 'atlas_consumer')
CONFIG_CENTER_ENABLED = os.getenv('CONFIG_CENTER_ENABLED', 'false')


def load_vault_settings(settings: BaseSettings) -> Dict[str, Any]:
    if CONFIG_CENTER_ENABLED == 'false':
        return {}
    else:
        vc = VaultClient(os.getenv('VAULT_URL'), os.getenv('VAULT_CRT'), os.getenv('VAULT_TOKEN'))
        return vc.get_from_vault(SRV_NAMESPACE)


class Settings(BaseSettings):
    """Store service configuration settings."""

    APP_NAME: str = 'lineage_consumer'
    VERSION: str = '0.2.3'

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

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return env_settings, load_vault_settings, init_settings, file_secret_settings

    def __init__(self) -> None:
        super().__init__()


ConfigClass = Settings()
