# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import LE_ADVERTISING_MANAGER_IFACE, RegistrationManager

import logging
logger = logging.getLogger(__name__)


class AdvertisementManager(RegistrationManager):
    def __init__(self, adapter):
        super().__init__(adapter, LE_ADVERTISING_MANAGER_IFACE,
                         'Advertisement')

    def advertise(self, advertisement):
        return self.register(advertisement)

    def unadvertise(self, advertisement):
        return self.unregister(advertisement)
