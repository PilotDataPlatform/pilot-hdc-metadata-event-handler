# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import asyncio
import logging

from fastapi import FastAPI

from metadata_event_handler.app.routers.v1.bulk_index.views import router as bulk_index_router
from metadata_event_handler.config import VERSION
from metadata_event_handler.consumer import MetadataConsumer

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Initialize and configure the application."""

    app = FastAPI(
        title='Metadata event handler',
        description='Service for spawning consumer and handling bulk indexing in Elasticsearch',
        docs_url='/v1/api-doc',
        redoc_url='/v1/api-redoc',
        version=VERSION,
    )

    setup_routers(app)

    @app.on_event('startup')
    async def startup_event():
        logger.info('Consumer started')
        consumer = MetadataConsumer()
        asyncio.create_task(consumer.run())

    return app


def setup_routers(app: FastAPI) -> None:
    """Configure the application routers."""
    app.include_router(bulk_index_router, prefix='/v1')
