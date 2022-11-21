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

ADVERTISEMENT_MANAGER = None


def get_advertisement_manager():
    global ADVERTISEMENT_MANAGER
    if ADVERTISEMENT_MANAGER is None:
        logger.debug('Creating singleton AdvertisementManager')
        ADVERTISEMENT_MANAGER = AdvertisementManager()
    return ADVERTISEMENT_MANAGER


from .scanned_advertisement import ScannedAdvertisement
from .scanner import Scanner

SCANNER = {}


def get_scanner(active=False):
    global SCANNER
    kind = 'active' if active else 'passive'
    if kind not in SCANNER:
        logger.debug(f'Creating singleton {kind} Scanner')
        SCANNER[kind] = Scanner(active=active)
    return SCANNER[kind]


def restart_scanners():
    global SCANNER
    for scanner in SCANNER.values():
        scanner.restart()


from .advertisement import Advertisement
from .peripheral import Peripheral
from .characteristic import Characteristic


__all__ = (
    get_advertisement_manager,
    get_scanner,
    restart_scanners,
    Advertisement,
    Characteristic,
    Peripheral,
    ScannedAdvertisement,
    )

__version__ = __version__
