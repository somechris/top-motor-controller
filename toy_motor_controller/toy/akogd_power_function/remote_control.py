# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.bus.bluez import Advertisement
from toy_motor_controller.util import randombyte


class AkogdPowerFunctionRemoteControl(Advertisement):
    def __init__(self):
        self._state = 1
        self._R = [randombyte() for i in range(3)]
        self._H = [0 for i in range(3)]
        self._M = [0 for i in range(4)]
        self._Z = [0 for i in range(6)]
        super(AkogdPowerFunctionRemoteControl, self).__init__()
        self._rebuild_data()

    def _rebuild_data(self):
        data = [0x67, self._state] + self._H + self._R + self._M + self._Z

        checksum = 0xe9
        for b in data:
            checksum ^= b
        data += [checksum]

        self._set_manufacturer_data(data)

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

    def set_motors(self, M):
        self._M = M
        self._rebuild_data()

    def __str__(self):
        r = ''.join([f'{i:02x}' for i in self._R])
        if self._state & 0x02:
            h = ''.join([f'{i:02x}' for i in self._H])
            m = ','.join([f'{i:02x}' for i in self._M])
            extra = f'connected, hub: {h}, motors: {m}'
        else:
            extra = 'unconnected'
        return f'AkogdRemoteControl(id: {r}, {extra})'
