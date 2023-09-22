# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import timezone

import faker
import pytest


class Faker(faker.Faker):
    def postgres_timestamp(self) -> int:
        datetime = self.date_time_this_year(tzinfo=timezone.utc)
        return datetime


@pytest.fixture
def fake(pytestconfig) -> Faker:
    seed = pytestconfig.getoption('random_order_seed', '0').lstrip('default:')

    fake = Faker()
    fake.seed_instance(seed=seed)
    fake.unique.clear()

    yield fake
