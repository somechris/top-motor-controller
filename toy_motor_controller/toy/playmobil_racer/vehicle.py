# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import copy
import threading

from toy_motor_controller.bus.bluez import AdvertisedApplication
from toy_motor_controller.bus.bluez import Service
from toy_motor_controller.bus.bluez import Characteristic
from toy_motor_controller.bus.bluez import get_object_interface
from toy_motor_controller.bus.bluez import DEVICE_IFACE
from toy_motor_controller.toy.common import CharacteristicIODiscovery

from . import PlaymobilRacerBase

from toy_motor_controller.util import normalize_mac_address

import logging
logger = logging.getLogger(__name__)


class PlaymobilRacerVehicle(PlaymobilRacerBase, CharacteristicIODiscovery,
                            AdvertisedApplication):
    def __init__(self):
        super().__init__()

        # Advertisement setup
        name = self.NAME_PREFIX + self.address[10:].replace(':', '')
        self._set_data(1, [6])
        self._set_data(9, bytes(name, 'utf-8'))

        # Application setup

        self._service = Service(self.SERVICE_UUID, primary=True)
        self.add(self._service)

        self.configure_discovery(
            application=self, service=self._service,
            uuid=self.CHARACTERISTIC_UUID)

        self._reset_state()
        self._state_change_listeners = []

    # -- Connection handling -------------------------------------------------

    def connect(self, address, supplement=None):
        address = normalize_mac_address(address)

        connection_lock = threading.Lock()
        connection_lock.acquire()  # Will be released in the characteristic
        # after the remote control connected

        characteristic = self.ReceiveCharacteristic(
            self.CHARACTERISTIC_UUID, address, self._update_state,
            connection_lock)
        self._service.add(characteristic)

        self.register()

        # Waiting for the remote control to connect.
        connection_lock.acquire()
        connection_lock.release()

        return super().connect()

    def disconnect(self):
        self.unregister()

        return super().disconnect()

    # -- Data handling -------------------------------------------------------

    def _reset_state(self):
        self._state = {
            'speed': 0,
            'light': 0,
            'speed_multiplier': 0,
            'direction': 0,
            }

    def _update_state(self, key, value):
        old_value = self._state[key]
        if old_value != value:
            old_state = copy.deepcopy(self._state)
            self._state[key] = value

            for listener in self._state_change_listeners:
                listener(state=self._state, old_state=old_state)

    def register_state_change(self, callback):
        self._state_change_listeners.append(callback)

    def unregister_state_change(self, callback):
        self._state_change_listeners.remove(callback)

    class ReceiveCharacteristic(Characteristic):
        def __init__(self, uuid, expected_address, state_updater,
                     connection_lock):
            super().__init__(
                uuid, write=True, write_without_response=True,
                notify=True)
            self._expected_address = expected_address
            self._state_updater = state_updater
            self._connection_lock = connection_lock

        def is_correct_device(self, address, device_path):
            if address == self._expected_address:
                return True

            # The request came from the wrong device, so we forcefully
            # disconnect.
            logger.debug(f'Disconnecting address {address}, as '
                         f'{self._expected_address} was expected')
            device = get_object_interface(device_path, DEVICE_IFACE)
            device.Disconnect()

            return False

        def write(self, value, address, offset, link, mtu, type_, device_path):
            if not self.is_correct_device(address, device_path):
                # Write came from wrong address
                return

            if self._connection_lock:
                # We're receiving from the correct device, so we're connected
                # and the vehicle is still waiting for the connection. So we
                # flag that we're connected by clearing the lock.
                self._connection_lock.release()
                self._connection_lock = None

            if len(value) != 3:
                # Command is too short
                return

            if value[2] != 0x0f:
                # Command is misformed
                return

            raw_key = value[0]
            raw_value = value[1]
            if raw_key == 0x23:
                state_key = 'speed'
                state_value = - 100 + int(raw_value * 200 / 255)
            elif raw_key == 0x24:
                state_key = 'light'
                state_value = 0 if raw_value == 1 else 100
            elif raw_key == 0x25:
                state_key = 'speed_multiplier'
                state_value = (raw_value - 1) * (255/4)
            elif raw_key == 0x40:
                state_key = 'direction'
                state_value = - 100 + int(raw_value * 200 / 255)
            else:
                # Faulty command
                return

            self._state_updater(state_key, state_value)
