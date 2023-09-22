# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from metadata_event_handler.app.routers.v1.bulk_index.utils import get_items_model
from metadata_event_handler.app.routers.v1.bulk_index.utils import parse_item_attributes
from metadata_event_handler.app.routers.v1.bulk_index.utils import update_item_template_info


def test_return_updated_item_with_template_info(get_items_response_single_page, get_project_template_response):
    item = get_items_response_single_page['result'][0]
    template = get_project_template_response[0]
    updated = update_item_template_info(item, {template['id']: template})
    assert updated['template_id'] == template['id']
    assert updated['template_name'] == template['name']


def test_return_updated_item_with_template_info_with_no_attributes(
    get_items_response_single_page, get_project_template_response
):
    item = get_items_response_single_page['result'][0]
    item['extended']['extra']['attributes'] = {}
    template = get_project_template_response[0]
    updated = update_item_template_info(item, {template['id']: template})
    assert updated['template_id'] is None
    assert updated['template_name'] is None


def test_return_parsed_item_attributes(fake, get_items_response_single_page, parse_item_response):
    item = get_items_response_single_page['result'][0]
    item['template_id'] = str(fake.uuid4())
    item['template_name'] = fake.pystr()
    parse_item_response['template_id'] = item['template_id']
    parse_item_response['template_name'] = item['template_name']
    parsed_items = parse_item_attributes(item)
    assert parsed_items == parse_item_response


def test_return_item_es_model(get_items_response_single_page, get_project_template_response, es_model):
    item = get_items_response_single_page['result'][0]
    template = get_project_template_response[0]
    model = get_items_model({item['id']: item}, {template['id']: template})
    assert model == es_model
