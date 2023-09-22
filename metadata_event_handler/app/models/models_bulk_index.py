# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime

from pydantic import BaseModel

from metadata_event_handler.app.models.base_models import APIResponse


class POSTItemsIndex(BaseModel):
    last_updated_start: datetime
    last_updated_end: datetime


class POSTItemsIndexResponse(APIResponse):
    pass
