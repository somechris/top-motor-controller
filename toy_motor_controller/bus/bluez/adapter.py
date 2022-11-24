# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus

from toy_motor_controller.bus.dbus import get_dbus

from . import SERVICE_NAME, ADAPTER_IFACE

import logging
logger = logging.getLogger(__name__)


class Adapter():
    def __init__(self, interfaces=[]):
        self._dbus = get_dbus()
        self._adapter = self._find_adapter(interfaces)
        self._configure_adapter()

    def _find_adapter(self, required_interfaces):
        bluez = self._dbus.get_object(SERVICE_NAME, '/')
        bluez_mos = self._dbus.get_om_iface(bluez).GetManagedObjects()

        for path, properties in bluez_mos.items():
            logger.debug(f'Trying Bluetooth adapter {path}')

            if all(required_interface in properties
                   for required_interface in required_interfaces):

                logger.debug(f'Picking Bluetooth adapter {path} as it meets '
                             f'{required_interfaces}')
                return self._dbus.get_object(SERVICE_NAME, path)

        raise RuntimeError('Failed to find adapter having all interfaces of '
                           f'{required_interfaces}')

    def _configure_adapter(self):
        adapter_props = self._dbus.get_props_iface(self._adapter)

        # Power on adapter
        adapter_props.Set(ADAPTER_IFACE, "Powered", dbus.Boolean(1))
        logger.debug('Bluetooth adapter is powered')

        # Fetch metadata
        self._metadata = {}
        for key in ['Address', 'AddressType', 'Name', 'Alias']:
            value = adapter_props.Get(ADAPTER_IFACE, key)
            logger.debug(f'Bluetooth adapter has {key} {value}')
            self._metadata[key] = value

    def get_interface(self, interface_name):
        return dbus.Interface(self._adapter, interface_name)

    def dbus_init_object(self, object, path):
        return self._dbus.init_object(object, path)

    @property
    def address(self):
        return self._metadata['Address']

    @property
    def address_type(self):
        return self._metadata['AddressType']

    @property
    def name(self):
        return self._metadata['Name']

    @property
    def alias(self):
        return self._metadata['Alias']
