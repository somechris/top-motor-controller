# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import time

from toy_motor_controller.bus.bluez import Characteristic
from toy_motor_controller.bus.bluez import get_object_interface
from toy_motor_controller.bus.bluez import DEVICE_IFACE


class CharacteristicIODiscovery(object):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._discovery_application = None
        self._discovery_service = None
        self._discovery_characteristic = None
        self._discovery_characteristic_uuid = None

        self._connected = False

    def configure_discovery(self, application, service, uuid):
        self._discovery_application = application
        self._discovery_service = service
        self._discovery_characteristic = None
        self._discovery_characteristic_uuid = uuid

    def scan(self, first=False, best=False, duration=10):
        matches_map = {}
        stop_time = (time.time() + duration) if duration is not None else 0

        if self._discovery_characteristic is None:
            self._discovery_characteristic = self.DiscoveryCharacteristic(
                self._discovery_characteristic_uuid, matches_map)
        self._discovery_service.add(self._discovery_characteristic)
        self._discovery_application.register()

        while not (first and matches_map) and \
                (not stop_time or time.time() < stop_time):
            time.sleep(0.1)

        self._discovery_service.remove(self._discovery_characteristic)
        self._discovery_application.unregister()

        matches = list(matches_map.values())

        if first or best:
            if matches:
                ret = matches[0]
            else:
                ret = None
        else:
            ret = matches

        return ret

    def connectFirst(self):
        scan_result = self.scan(first=True)
        if scan_result is None:
            raise RuntimeError('Failed to find connectable device')
        return self.connect(**scan_result)

    def connectBest(self, duration=10):
        scan_result = self.scan(best=True, duration=duration)
        if scan_result is None:
            raise RuntimeError('Failed to find connectable device')
        return self.connect(**scan_result)

    def connect(self):
        self._connected = True

        return self

    def disconnect(self):
        self._connected = False

        return self

    class DiscoveryCharacteristic(Characteristic):
        def __init__(self, uuid, matches_map):
            super().__init__(
                uuid, indicate=True, read=True, notify=True, write=True,
                write_without_response=True)

            self._matches_map = matches_map

        def record_device(self, address, device_path):
            try:
                self._matches_map['address'] = {
                    'address': address
                    }
                device = get_object_interface(device_path, DEVICE_IFACE)
                device.Disconnect()
            except Exception as e:
                print(e)

        def read(self, address, offset, link, mtu, type_, device_path):
            self.record_device(address, device_path)
            return []

        def write(self, value, address, offset, link, mtu, type_, device_path):
            self.record_device(address, device_path)
