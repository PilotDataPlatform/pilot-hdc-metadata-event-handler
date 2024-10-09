# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import uvicorn

from metadata_event_handler.config import HOST
from metadata_event_handler.config import PORT
from metadata_event_handler.config import WORKERS

if __name__ == '__main__':
    uvicorn.run('metadata_event_handler.main:create_app', factory=True, host=HOST, port=PORT, workers=WORKERS)
