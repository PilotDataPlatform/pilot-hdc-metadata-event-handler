# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest

from metadata_event_handler.filtering import MetadataItemFacetFiltering


class TestFiltering:
    def test_return_filtered_message(self, item_message, filtered_item):
        filtered_message = MetadataItemFacetFiltering(item_message).apply()
        assert filtered_message.to_dict() == filtered_item

    def test_invalid_type_for_item_facet_model_return_value_error(self, item_message, filtered_item):
        item_message['type'] = 'name_folder'
        with pytest.raises(ValueError):
            MetadataItemFacetFiltering(item_message).apply()

    def test_invalid_zone_for_item_facet_model_return_value_error(self, item_message, filtered_item):
        item_message['zone'] = 3
        with pytest.raises(ValueError):
            MetadataItemFacetFiltering(item_message).apply()

    def test_return_filtered_message_with_no_specified_parent_path(self, item_message, filtered_item):
        item_message['parent_path'] = None
        filtered_item['parent_path'] = None
        filtered_message = MetadataItemFacetFiltering(item_message).apply()
        assert filtered_message.to_dict() == filtered_item

    def test_return_filtered_message_with_no_specified_template_name(self, item_message, filtered_item):
        item_message['extended']['template_name'] = None
        filtered_item['template_name'] = None
        filtered_message = MetadataItemFacetFiltering(item_message).apply()
        assert filtered_message.to_dict() == filtered_item
