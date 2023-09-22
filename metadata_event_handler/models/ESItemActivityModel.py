# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

class ESItemActivityModel:
    def __init__(self):
        self.activity_type = ''
        self.activity_time = ''
        self.item_id = ''
        self.item_type = ''
        self.item_name = ''
        self.item_parent_path = ''
        self.container_code = ''
        self.container_type = ''
        self.zone = 0
        self.user = ''
        self.imported_from = ''
        self.changes = []

    def to_dict(self) -> dict:
        return {
            'activity_type': self.activity_type,
            'activity_time': self.activity_time,
            'item_id': self.item_id,
            'item_type': self.item_type,
            'item_name': self.item_name,
            'item_parent_path': self.item_parent_path,
            'container_code': self.container_code,
            'container_type': self.container_type,
            'zone': self.zone,
            'user': self.user,
            'imported_from': self.imported_from,
            'changes': self.changes,
        }
