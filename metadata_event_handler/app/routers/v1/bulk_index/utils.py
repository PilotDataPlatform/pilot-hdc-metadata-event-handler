# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from datetime import timezone
from typing import Any

from metadata_event_handler.models.ESItemModel import ESItemModel


def convert_date_to_timestamp(date: str) -> int:
    date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=timezone.utc)
    return int(date_time.timestamp())


def parse_item_attributes(item: dict) -> dict:
    """Parse item to flatten structure for Elasticsearch Item Model."""
    parsed = {}
    for k, v in item.items():
        if k == 'storage':
            parsed[f'{k}_id'] = v['id']
            parsed['location_uri'] = v['location_uri']
            parsed['version'] = v['version']
        elif k == 'extended':
            parsed[f'{k}_id'] = v['id']
            parsed['tags'] = v['extra']['tags']
            parsed['system_tags'] = v['extra']['system_tags']
            parsed['attributes'] = v['extra']['attributes']
        elif k in ['created_time', 'last_updated_time']:
            parsed[k] = convert_date_to_timestamp(v)
        else:
            parsed[k] = v
        parsed['to_delete'] = False
    return parsed


def update_item_template_info(item_value: dict[str:Any], template_info: dict[str:Any]) -> dict[str, Any]:
    """Attach template characteristics to each item."""
    attributes = item_value['extended']['extra']['attributes']
    if attributes:
        template_id = next(iter(attributes))
        template_matched = template_info[template_id]
        template_name = template_matched['name']
        item_value['template_id'] = template_id
        item_value['template_name'] = template_name
        item_value['attributes'] = attributes[template_id]
    else:
        item_value['template_id'] = None
        item_value['template_name'] = None
    return item_value


def get_items_model(items: dict[str:Any], template_info: dict[str:Any]) -> dict[str:Any]:
    """Translate item dictionary into Elasticsearch Item Model."""
    items_model = {}
    for item_id, value in items.items():
        model = ESItemModel()
        updated_item = update_item_template_info(value, template_info)
        item_dict = parse_item_attributes(updated_item)
        model_attrs = model.to_dict().keys()
        for attr in model_attrs:
            setattr(model, attr, item_dict[attr])
        items_model[item_id] = model.to_dict()
    return items_model
