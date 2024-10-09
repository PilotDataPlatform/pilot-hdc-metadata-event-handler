# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

pytest_plugins = [
    'tests.fixtures.clients.elasticsearch',
    'tests.fixtures.services.metadata',
    'tests.fixtures.services.project',
    'tests.fixtures.event',
    'tests.fixtures.fake',
    'tests.fixtures.main',
    'tests.fixtures.router_utils',
    'tests.fixtures.filtering',
]
