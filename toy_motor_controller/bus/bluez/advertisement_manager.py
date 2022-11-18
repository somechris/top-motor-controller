# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import threading

import dbus

from toy_motor_controller.bus.dbus import get_dbus

from . import SERVICE_NAME, ADAPTER_IFACE, LE_ADVERTISING_MANAGER_IFACE

import logging
logger = logging.getLogger(__name__)

ADVERTISEMENT_BASE_PATH = '/org/bluez/example/advertisement'


class AdvertisementManager():
    def __init__(self):
        logger.debug('Bringing up AdvertisementManager ...')
        self._dbus = get_dbus()

        bluez = self._dbus.get_object(SERVICE_NAME, '/')
        bluez_mos = self._dbus.get_om_iface(bluez).GetManagedObjects()

        adapter_path = None
        adapter_props = None
        for mo, props in bluez_mos.items():
            if not adapter_path:
                if LE_ADVERTISING_MANAGER_IFACE in props:
                    adapter_path = mo

        adapter = self._dbus.get_object(SERVICE_NAME, adapter_path)
        adapter_props = self._dbus.get_props_iface(adapter)

        # Power on adapter
        adapter_props.Set(ADAPTER_IFACE, "Powered", dbus.Boolean(1))
        logger.debug('Bluetooth adapter is powered')

        # Fetch address
        self._data = {}
        for key in ['Address', 'AddressType', 'Name', 'Alias']:
            value = adapter_props.Get(ADAPTER_IFACE, key)
            logger.debug(f'Bluetooth adapter has {key} {value}')
            self._data[key] = value

        self._manager = dbus.Interface(adapter, LE_ADVERTISING_MANAGER_IFACE)

        self._advertisements = {}
        logger.debug('AdvertisementManager is up and running')

    def manage(self, advertisement):
        if advertisement not in self._advertisements:
            logger.debug(f'Starting to manage {advertisement}')
            path = ADVERTISEMENT_BASE_PATH \
                + str(len(self._advertisements.keys()))
            self._dbus.init_object(advertisement, path)
            properties = {
                'path': path,
                'lock': threading.Lock(),
                'advertised': False,
                }
            self._advertisements[advertisement] = properties

    def unadvertise(self, advertisement):
        properties = self._advertisements[advertisement]
        if properties['advertised']:
            with properties['lock']:
                if properties['advertised']:
                    self._unadvertise(properties)

    def _unadvertise(self, properties):
        path = properties['path']
        logger.debug(f'Unadvertising {path}')
        self._manager.UnregisterAdvertisement(path)
        properties['advertised'] = False

    def advertise(self, advertisement):
        properties = self._advertisements[advertisement]
        if not properties['advertised']:
            properties['lock'].acquire()
            if not properties['advertised']:
                self._advertise(properties)
            else:
                properties['lock'].release()

    def _advertise(self, properties):
        path = properties['path']

        def cleanup():
            properties['lock'].release()

        def advertizing_worked():
            properties['advertised'] = True
            logger.debug(f'Registering {path} done')
            cleanup()

        def advertizing_failed(error):
            logger.debug(f'Registering {path} failed: {error}')
            cleanup()

        self._manager.RegisterAdvertisement(
            path, {},
            reply_handler=advertizing_worked,
            error_handler=advertizing_failed)

    def update(self, advertisement):
        logger.debug(f'Updating {advertisement}')

        properties = self._advertisements[advertisement]
        if properties['advertised']:
            properties['lock'].acquire()
            if properties['advertised']:
                self._unadvertise(properties)
                self._advertise(properties)
            else:
                properties['lock'].release()

    @property
    def address(self):
        return self._data['Address']

    @property
    def address_type(self):
        return self._data['AddressType']

    @property
    def name(self):
        return self._data['Name']

    @property
    def alias(self):
        return self._data['Alias']
