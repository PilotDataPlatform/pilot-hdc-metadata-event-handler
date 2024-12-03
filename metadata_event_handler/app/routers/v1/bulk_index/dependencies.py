# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import Depends

from metadata_event_handler.app.dependencies import get_elasticsearch_client
from metadata_event_handler.app.routers.v1.bulk_index.crud import BulkIndexItems
from metadata_event_handler.clients.elasticsearch import ElasticsearchClient
from metadata_event_handler.config import METADATA_SERVICE
from metadata_event_handler.config import PROJECT_SERVICE
from metadata_event_handler.services.metadata import MetadataService
from metadata_event_handler.services.project import ProjectService


def get_metadata_service() -> MetadataService:
    """Create a callable dependency for MetadataService instance."""
    return MetadataService(METADATA_SERVICE)


def get_project_service() -> ProjectService:
    """Create a callable dependency for ProjectService instance."""
    return ProjectService(PROJECT_SERVICE)


es_client = get_elasticsearch_client()
metadata_service = get_metadata_service()


def get_bulk_index_crud(
    elasticsearch_client: ElasticsearchClient = Depends(get_elasticsearch_client),
    metadata_client: MetadataService = Depends(get_metadata_service),
    project_client: ProjectService = Depends(get_project_service),
) -> BulkIndexItems:
    """Return an instance of BulkIndexItems as a dependency."""

    return BulkIndexItems(elasticsearch_client, metadata_client, project_client)
