# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import APIRouter
from fastapi import Depends
from starlette.responses import JSONResponse

from metadata_event_handler.app.models.base_models import EAPIResponseCode
from metadata_event_handler.app.models.models_bulk_index import POSTItemsIndex
from metadata_event_handler.app.models.models_bulk_index import POSTItemsIndexResponse
from metadata_event_handler.app.routers.router_exceptions import ItemsNotFoundException
from metadata_event_handler.app.routers.router_exceptions import UnhandledException
from metadata_event_handler.app.routers.v1.bulk_index.crud import BulkIndexItems
from metadata_event_handler.app.routers.v1.bulk_index.dependencies import get_bulk_index_crud
from metadata_event_handler.logger import logger

router = APIRouter(prefix='/event-handler', tags=['Bulk Index'])


@router.post(
    '/bulk-index',
    summary='Bulk index metadata items updated between date range into Elasticsearch',
    response_model=POSTItemsIndexResponse,
)
async def execute_bulk_index(
    request: POSTItemsIndex, get_bulk_index_crud: BulkIndexItems = Depends(get_bulk_index_crud)
) -> JSONResponse:
    """Bulk index project metadata items into Elasticsearch between date-range."""
    response = POSTItemsIndexResponse()
    try:
        await get_bulk_index_crud.bulk_upsert(
            start_time=request.last_updated_start,
            end_time=request.last_updated_end,
        )
        response.code = EAPIResponseCode.success
    except ItemsNotFoundException:
        response.code = EAPIResponseCode.not_found
        response.error_msg = 'No items found in metadata service for date-range'
    except UnhandledException:
        logger.exception('Unexpected Internal Server Error')
        response.code = EAPIResponseCode.internal_error
        response.error_msg = 'Unexpected Internal Server Error'
    except Exception:
        logger.exception('Failure to bulk index')
        response.code = EAPIResponseCode.internal_error
        response.error_msg = 'Bulk indexing failed'
    return response.json_response()
