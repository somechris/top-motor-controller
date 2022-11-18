# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .. import __version__

import logging
logger = logging.getLogger(__name__)

SERVICE_NAME = 'org.bluez'
ADAPTER_IFACE = 'org.bluez.Adapter1'

LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

from .advertisement_manager import AdvertisementManager
from .characteristic import Characteristic

ADVERTISEMENT_MANAGER = None


def get_advertisement_manager():
    global ADVERTISEMENT_MANAGER
    if ADVERTISEMENT_MANAGER is None:
        logger.debug('Creating singleton AdvertisementManager')
        ADVERTISEMENT_MANAGER = AdvertisementManager()
    return ADVERTISEMENT_MANAGER


from .scanned_advertisement import ScannedAdvertisement
from .scanner import Scanner

SCANNER = None


def get_scanner():
    global SCANNER
    if SCANNER is None:
        logger.debug('Creating singleton Scanner')
        SCANNER = Scanner()
    return SCANNER


from .advertisement import Advertisement


__all__ = (
    get_advertisement_manager,
    get_scanner,
    Advertisement,
    Characteristic,
    ScannedAdvertisement,
    )

__version__ = __version__
