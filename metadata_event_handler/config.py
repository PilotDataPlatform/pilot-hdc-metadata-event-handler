# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
import logging
import os
from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv

load_dotenv('.env')
KAFKA_SERVICE = os.getenv('KAFKA_SERVICE', None)
KAFKA_TOPICS = json.loads(os.getenv('KAFKA_TOPICS', '[]'))
KAFKA_SCHEMAS_PATH = Path(__file__).parent / 'kafka_schemas'
ELASTICSEARCH_SERVICE = os.getenv('ELASTICSEARCH_SERVICE', None)
APP_NAME = os.getenv('APP_NAME', None)
VERSION = os.getenv('VERSION', None)
HOST = os.getenv('HOST', None)
PORT = int(os.getenv('PORT', 5063))
WORKERS = int(os.getenv('WORKERS', 1))
METADATA_SERVICE = os.getenv('METADATA_SERVICE', 'http://METADATA_SERVICE:1010')
PROJECT_SERVICE = os.getenv('PROJECT_SERVICE', 'http://PROJECT_SERVICE:1010')
METADATA_SERVICE_PAGE_SIZE = os.getenv('METADATA_SERVICE_PAGE_SIZE', 50)
PROJECT_SERVICE_PAGE_SIZE = os.getenv('METADATA_SERVICE_PAGE_SIZE', 100)
ELASICSEARCH_PAGE_SIZE = os.getenv('ELASICSEARCH_PAGE_SIZE', 50)
CONSUMER_GROUP = os.getenv('CONSUMER_GROUP', 'metadata-event-handler')
SEEK_TO_BEGINNING = bool(strtobool(os.getenv('SEEK_TO_BEGINNING', 'False')))
LOGGING_LEVEL = int(os.getenv('LOGGING_LEVEL', logging.INFO))
LOGGING_FORMAT = os.getenv('APP_NAME', 'json')
