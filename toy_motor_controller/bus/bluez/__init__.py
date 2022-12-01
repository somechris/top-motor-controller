# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .. import __version__

from toy_motor_controller.util import singleton_getter
from toy_motor_controller.util import get_fully_qualified_name
from toy_motor_controller.bus.dbus import get_dbus_object_registry

import logging
logger = logging.getLogger(__name__)

SERVICE_NAME = 'org.bluez'
ADAPTER_IFACE = 'org.bluez.Adapter1'

LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
LE_ADVERTISEMENT_IFACE = 'org.bluez.LEAdvertisement1'

GATT_MANAGER_IFACE = 'org.bluez.GattManager1'
GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHARACTERISTIC_IFACE = 'org.bluez.GattCharacteristic1'
GATT_DESCRIPTOR_IFACE = 'org.bluez.GattDescriptor1'

from .util import convert_device_object_path_to_mac_address
from .util import normalize_io_options

from .adapter import Adapter
from .registration_error import RegistrationError
from .registration_manager import RegistrationManager
from .advertisement_manager import AdvertisementManager
from .application_manager import ApplicationManager

get_adapter = singleton_getter(
    Adapter, lambda: ([LE_ADVERTISING_MANAGER_IFACE, GATT_MANAGER_IFACE],))
get_advertisement_manager = singleton_getter(
    AdvertisementManager, lambda: (get_adapter(),))
get_application_manager = singleton_getter(
    ApplicationManager, lambda: (get_adapter(),))

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


from .registree import Registree
from .advertisement import Advertisement
from .peripheral import Peripheral
from .application import Application
from .service import Service
from .characteristic import Characteristic
from .descriptor import Descriptor
from .advertised_application import AdvertisedApplication
from .logging_characteristic import LoggingCharacteristic

dbus_object_registry = get_dbus_object_registry()
dbus_object_registry.map_name(
    get_fully_qualified_name(Advertisement),
    'advertisement')
dbus_object_registry.map_name(
    get_fully_qualified_name(Application),
    'application')
dbus_object_registry.map_name(
    get_fully_qualified_name(Characteristic),
    'characteristic')
dbus_object_registry.map_name(
    get_fully_qualified_name(Descriptor),
    'descriptor')
dbus_object_registry.map_name(
    get_fully_qualified_name(Service),
    'service')

__all__ = (
    convert_device_object_path_to_mac_address,
    get_advertisement_manager,
    get_application_manager,
    get_scanner,
    get_scanner_active,
    get_scanner_passive,
    normalize_io_options,
    restart_scanners,
    Advertisement,
    AdvertisedApplication,
    Application,
    Characteristic,
    Descriptor,
    LoggingCharacteristic,
    Peripheral,
    Registree,
    RegistrationManager,
    RegistrationError,
    ScannedAdvertisement,
    Service,
    )

__version__ = __version__
