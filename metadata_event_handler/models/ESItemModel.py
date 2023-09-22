# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from enum import Enum


class ItemStatus(str, Enum):
    """The new enum type for file status.

    - REGISTERED means file is created by upload service but not complete yet. either in progress or fail.
    - ACTIVE means file uploading is complete.
    - ARCHIVED means the file has been deleted.
    """

    REGISTERED = 'REGISTERED'
    ACTIVE = 'ACTIVE'
    ARCHIVED = 'ARCHIVED'

    def __str__(self):
        return '%s' % self.name


class ESItemModel:
    def __init__(self):
        self.id = ''
        self.parent = ''
        self.parent_path = ''
        self.restore_path = ''
        self.status = ItemStatus.REGISTERED
        self.type = ''
        self.zone = 0
        self.name = ''
        self.size = 0
        self.owner = ''
        self.container_code = ''
        self.container_type = ''
        self.created_time = ''
        self.last_updated_time = ''
        self.to_delete = False
        self.storage_id = ''
        self.location_uri = ''
        self.version = ''
        self.extended_id = ''
        self.tags = []
        self.system_tags = []
        self.template_name = ''
        self.template_id = None
        self.attributes = {}

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'parent': self.parent,
            'parent_path': self.parent_path,
            'restore_path': self.restore_path,
            'status': self.status,
            'type': self.type,
            'zone': self.zone,
            'name': self.name,
            'size': self.size,
            'owner': self.owner,
            'container_code': self.container_code,
            'container_type': self.container_type,
            'created_time': self.created_time,
            'last_updated_time': self.last_updated_time,
            'to_delete': self.to_delete,
            'storage_id': self.storage_id,
            'location_uri': self.location_uri,
            'version': self.version,
            'extended_id': self.extended_id,
            'tags': self.tags,
            'system_tags': self.system_tags,
            'template_name': self.template_name,
            'template_id': self.template_id,
            'attributes': self.attributes,
        }
