# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.bus.bluez import Characteristic
from toy_motor_controller.bus.bluez import get_object_interface
from toy_motor_controller.bus.bluez import DEVICE_IFACE

from . import DiscoveryBase


class CharacteristicIODiscovery(DiscoveryBase):
    # -- Initialization ------------------------------------------------------

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.configure_discovery(None, None, None)

    def configure_discovery(self, application, service, uuid):
        self._discovery_application = application
        self._discovery_service = service
        self._discovery_characteristic_uuid = uuid

    # -- Scanning ------------------------------------------------------------

    def _start_scan(self, matches_map):
        characteristic = self.DiscoveryCharacteristic(
            self._discovery_characteristic_uuid, matches_map)
        self._discovery_service.add(characteristic)
        self._discovery_application.register()

        return {'characteristic': characteristic}

    def _stop_scan(self, scan_state):
        self._discovery_service.remove(scan_state['characteristic'])
        self._discovery_application.unregister()

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
