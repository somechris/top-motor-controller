# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.bus.bluez import Advertisement
from toy_motor_controller.control import uint8_standardized_control
from toy_motor_controller.util import randombyte


class AkogdPowerFunctionRemoteControl(Advertisement):

    # -- Initialization ------------------------------------------------------

    def __init__(self):
        self._state = 1
        self._R = [randombyte() for i in range(3)]
        self._H = [0 for i in range(3)]
        self._M = [0 for i in range(4)]
        self._Z = [0 for i in range(6)]
        super(AkogdPowerFunctionRemoteControl, self).__init__()
        self._rebuild_data()

    # -- Connection handling -------------------------------------------------

    def connected(self, H):
        self._state = 2
        self._H = H
        self._M = [0x80 for i in range(4)]
        self._rebuild_data()

    def disconnected(self):
        self._state = 1
        self._H = [0 for i in range(3)]
        self._M = [0 for i in range(4)]
        self._rebuild_data()

    # -- Data sending --------------------------------------------------------

    def _rebuild_data(self):
        data = [0x67, self._state] + self._H + self._R + self._M + self._Z

        checksum = 0xe9
        for b in data:
            checksum ^= b
        data += [checksum]

        self._set_manufacturer_data(data)

    # -- Raw setter ----------------------------------------------------------

    def _set_port(self, port, value):
        self._M[port] = value
        self._rebuild_data()

    # -- User setter ---------------------------------------------------------

    @uint8_standardized_control(
        'Port A (0=full speed counter-clockwise, 100=full speed clockwise)')
    def a(self, value):
        print('setting', value)
        self._set_port(0, value)

    @uint8_standardized_control(
        'Port B (0=full speed counter-clockwise, 100=full speed clockwise)')
    def b(self, value):
        self._set_port(1, value)

    @uint8_standardized_control(
        'Port C (0=full speed counter-clockwise, 100=full speed clockwise)')
    def c(self, value):
        self._set_port(2, value)

    @uint8_standardized_control(
        'Port D (0=full speed counter-clockwise, 100=full speed clockwise)')
    def d(self, value):
        self._set_port(3, value)

    # -- Utilities -----------------------------------------------------------

    def __str__(self):
        r = ''.join([f'{i:02x}' for i in self._R])
        if self._state & 0x02:
            h = ''.join([f'{i:02x}' for i in self._H])
            m = ','.join([f'{i:02x}' for i in self._M])
            extra = f'connected, hub: {h}, motors: {m}'
        else:
            extra = 'unconnected'
        return f'AkogdRemoteControl(id: {r}, {extra})'
