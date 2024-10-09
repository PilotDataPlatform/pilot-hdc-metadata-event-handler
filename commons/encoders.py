# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime


def convert_datetime_to_timestamp_millisecond(date: datetime) -> int:
    """Translate datetime to timestamp in milliseconds.

    :param date: Date
    :return: Timestamp in milliseconds
    """
    return int(date.timestamp() * 1000)


datetime_as_timestamp_milli_encoder = {
    datetime: convert_datetime_to_timestamp_millisecond,
}
