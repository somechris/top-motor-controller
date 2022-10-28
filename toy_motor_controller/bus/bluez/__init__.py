# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import logging
logger = logging.getLogger(__name__)

SERVICE_NAME = 'org.bluez'
ADAPTER_IFACE = 'org.bluez.Adapter1'

LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

from .advertisement_manager import AdvertisementManager

ADVERTISEMENT_MANAGER = None


def get_advertisement_manager():
    global ADVERTISEMENT_MANAGER
    if ADVERTISEMENT_MANAGER is None:
        logger.debug('Creating singleton AdvertisementManager')
        ADVERTISEMENT_MANAGER = AdvertisementManager()
    return ADVERTISEMENT_MANAGER


from .advertisement import Advertisement


__all__ = (
    get_advertisement_manager,
    Advertisement,
    )
