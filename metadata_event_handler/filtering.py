# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any

from metadata_event_handler.models.ESItemFacetModel import ESItemFacetModel
from metadata_event_handler.models.ESItemModel import ItemStatus


class MetadataItemFacetFiltering:
    """Metadata items filtering for faceted search."""

    def __init__(self, message: dict[str, Any]):
        self.message = message

    def apply(self) -> ESItemFacetModel:
        """Filter items by validated fields.

        :return: ESItemFacetModel with validated fields.
        """
        item = {
            'container_code': self.message['container_code'],
            'created_time': self.message['created_time'],
            'identifier': str(self.message['id']),
            'last_updated_time': self.message['last_updated_time'],
            'name': self.message['name'],
            'owner': self.message['owner'],
            'parent_path': self.message['parent_path'],
            'size': self.message['size'],
            'system_tags': self.message['extended']['extra']['system_tags'],
            'tags': self.message['extended']['extra']['tags'],
            'template_name': self.message['extended']['template_name'],
            'type': self.message['type'],
            'zone': self.message['zone'],
            'zonefilter': self.message['zone'],
            'to_delete': True if self.message['status'] == ItemStatus.ARCHIVED else self.message['to_delete'],
        }
        es_item = ESItemFacetModel(**item)
        return es_item
