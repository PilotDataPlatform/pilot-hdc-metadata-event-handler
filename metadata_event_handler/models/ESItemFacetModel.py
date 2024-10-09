# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import validator

from commons.encoders import datetime_as_timestamp_milli_encoder


class ESItemFacetModel(BaseModel):
    """Schema for item faceted search elasticsearch index."""

    container_code: str
    created_time: datetime
    identifier: str
    last_updated_time: datetime
    name: str
    owner: str
    parent_path: Optional[str] = None
    size: int
    system_tags: list
    tags: list
    template_name: Optional[str] = None
    type: str
    zone: int
    zonefilter: int
    to_delete: bool = False

    @validator('type')
    def validate_type(cls, v):
        if v == 'name_folder':
            raise ValueError('name_folder should be excluded from faceted search')
        return v

    @validator('parent_path')
    def validate_parent_path(cls, v):
        if v is None:
            return None
        return v

    @validator('zone', 'zonefilter')
    def validate_zone(cls, v):
        if v not in [0, 1]:
            raise ValueError('zone is invalid')
        zone_str = 'greenroom' if v == 0 else 'core'
        return zone_str

    @validator('template_name')
    def validate_template_name(cls, v):
        if v is None:
            return None
        return v

    def to_dict(self) -> dict:
        return json.loads(self.json())

    class Config:
        json_encoders = datetime_as_timestamp_milli_encoder
