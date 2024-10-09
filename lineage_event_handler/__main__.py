# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import asyncio

from common import configure_logging

from lineage_event_handler.config import ConfigClass
from lineage_event_handler.consumer import LineageConsumer
from lineage_event_handler.logger import logger

if __name__ == '__main__':
    configure_logging(ConfigClass.LOGGING_LEVEL, ConfigClass.LOGGING_FORMAT)
    logger.info('Lineage event handler started')
    consumer = LineageConsumer()
    asyncio.run(consumer.run())
