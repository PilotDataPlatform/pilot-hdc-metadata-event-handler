# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

class ESDatasetActivityModel:
    def __init__(self):
        self.activity_type = ''
        self.activity_time = ''
        self.container_code = ''
        self.user = ''
        self.target_name = ''
        self.version = ''
        self.changes = []

    def to_dict(self) -> dict:
        return {
            'activity_type': self.activity_type,
            'activity_time': self.activity_time,
            'container_code': self.container_code,
            'user': self.user,
            'target_name': self.target_name,
            'version': self.version,
            'changes': self.changes,
        }
