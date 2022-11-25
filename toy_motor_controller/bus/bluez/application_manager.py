# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import GATT_MANAGER_IFACE, RegistrationManager

import logging
logger = logging.getLogger(__name__)


class ApplicationManager(RegistrationManager):
    def __init__(self, adapter):
        super().__init__(adapter, GATT_MANAGER_IFACE,
                         'Application')
