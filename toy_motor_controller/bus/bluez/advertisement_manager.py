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

        # Fetch address (which is only used for debugging)
        for key in ['Address', 'Name', 'Alias']:
            value = adapter_props.Get(ADAPTER_IFACE, "Address")
            logger.debug(f'Bluetooth adapter has {key} {value}')

        self._manager = dbus.Interface(adapter, LE_ADVERTISING_MANAGER_IFACE)

        self._advertisements = {}
        logger.debug('AdvertisementManager is up and running')

    def _manage(self, advertisement):
        logger.debug(f'Starting to manage {advertisement}')
        path = ADVERTISEMENT_BASE_PATH + str(len(self._advertisements.keys()))
        self._dbus.init_object(advertisement, path)
        adv_props = {
            'path': path,
            'lock': threading.Lock()
            }
        self._advertisements[advertisement] = adv_props

        return adv_props

    def _unadvertise(self, adv_props):
        path = adv_props['path']
        try:
            self._manager.UnregisterAdvertisement(path)
        except dbus.exceptions.DBusException as e:
            if e.get_dbus_name() == 'org.bluez.Error.DoesNotExist':
                # The path was not published. So it was unpublished already
                logger.debug(f'Unadvertized not existing path {path}')
            else:
                raise e

    def _advertise(self, adv_props):
        path = adv_props['path']

        def cleanup():
            adv_props['lock'].release()

        def advertizing_worked():
            logger.debug(f'Registering {path} done')
            cleanup()

        def advertizing_failed(error):
            logger.debug(f'Registering {path} failed: {error}')
            cleanup()

        self._manager.RegisterAdvertisement(
            path, {},
            reply_handler=advertizing_worked,
            error_handler=advertizing_failed)

    def republish(self, advertisement):
        logger.debug(f'Republishing {advertisement}')
        try:
            adv_props = self._advertisements[advertisement]
        except KeyError:
            adv_props = self._manage(advertisement)

        path = adv_props['path']

        adv_props['lock'].acquire()

        logger.debug(f'  Unadvertising {path}')
        self._unadvertise(adv_props)
        logger.debug(f'  Advertising {path}')
        self._advertise(adv_props)
        logger.debug(f'Republishing {advertisement} done')
