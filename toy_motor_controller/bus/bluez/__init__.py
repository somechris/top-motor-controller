# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .. import __version__

from toy_motor_controller.util import singleton_getter

import logging
logger = logging.getLogger(__name__)

SERVICE_NAME = 'org.bluez'
ADAPTER_IFACE = 'org.bluez.Adapter1'

LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

REGISTRATION_MANAGER_BASE_PATH = '/org/bluez/example'

from .adapter import Adapter
from .registration_error import RegistrationError
from .registration_manager import RegistrationManager
from .advertisement_manager import AdvertisementManager

get_adapter = singleton_getter(
    Adapter, lambda: ([LE_ADVERTISING_MANAGER_IFACE],))
get_advertisement_manager = singleton_getter(
    AdvertisementManager, lambda: (get_adapter(),))

from .scanned_advertisement import ScannedAdvertisement
from .scanner import Scanner

SCANNER = {}

get_scanner_active = singleton_getter(
    Scanner, lambda: {'active': True}, 'active', SCANNER)
get_scanner_passive = singleton_getter(
    Scanner, lambda: {'active': False}, 'passive', SCANNER)


def get_scanner(active=False):
    if active:
        return get_scanner_active()
    return get_scanner_passive()


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
    get_scanner_active,
    get_scanner_passive,
    restart_scanners,
    Advertisement,
    Characteristic,
    Peripheral,
    RegistrationManager,
    RegistrationError,
    ScannedAdvertisement,
    )

__version__ = __version__
