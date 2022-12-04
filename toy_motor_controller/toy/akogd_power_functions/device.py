# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.bus.bluez import Advertisement
from toy_motor_controller.toy.common import BluetoothAdvertisementDiscovery
from toy_motor_controller.util import bytes_to_hex_string


class AkogdPowerFunctionsDevice(BluetoothAdvertisementDiscovery,
                                Advertisement):

    # -- Initialization ------------------------------------------------------

    def __init__(self):
        self._magic = [0x00, 0x00, 0x67]
        self._magic_str = bytes_to_hex_string(self._magic)
        self._connection_state = 0
        self._H = [0 for i in range(3)]
        self._R = [0 for i in range(3)]
        self._M = [0 for i in range(4)]
        self._Z = [0 for i in range(6)]

        super().__init__()

    # -- Data sending --------------------------------------------------------

    def _rebuild_data(self):
        data = self._magic + [self._connection_state] + self._H + self._R \
            + self._M + self._Z

        checksum = 0xe9
        for b in data:
            checksum ^= b
        data += [checksum]

        self._set_manufacturer_data(data)

    def connect(self):
        self._rebuild_data()

        return super().connect()

    def disconnect(self):
        self._rebuild_data()

        return super().disconnect()

    # -- Utilities -----------------------------------------------------------

    def __str__(self):
        s = bytes_to_hex_string([self._connection_state])
        h = bytes_to_hex_string(self._H)
        r = bytes_to_hex_string(self._R)
        m = bytes_to_hex_string(self._M, connector=',')
        connected = 'connected' if (self._connected) else 'unconnected'
        return f'{self.__class__.__name__}({connected}, '\
            f'state: {s}, h: {h}, r: {r}, h: {h}, m: {m})'
