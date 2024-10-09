# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.


class ItemsNotFoundException(Exception):
    """Raised when no items from metadata service."""

    pass


class ServiceNotAvailable(Exception):
    """Raised when external service is not available."""


class UnhandledException(Exception):
    """Raised when unhandled/unexpected internal error occurred."""
