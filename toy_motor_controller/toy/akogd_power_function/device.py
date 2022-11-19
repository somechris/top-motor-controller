# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import time

from toy_motor_controller.bus.bluez import Advertisement, get_scanner
from toy_motor_controller.util import bytes_to_hex_string


class AkogdPowerFunctionDevice(Advertisement):

    # -- Initialization ------------------------------------------------------

    def __init__(self):
        self._magic = [0x00, 0x00, 0x67]
        self._magic_str = bytes_to_hex_string(self._magic)
        self._connection_state = 0
        self._H = [0 for i in range(3)]
        self._R = [0 for i in range(3)]
        self._M = [0 for i in range(4)]
        self._Z = [0 for i in range(6)]
        self._connected = False
        self._scanner = get_scanner()

        super().__init__(advertise=False)

    # -- Connection handling -------------------------------------------------

    def _get_scanning_callback(self, matches_map):
        raise NotImplementedError()

    def scan(self, first=False, best=False, duration=10):
        matches_map = {}
        stop_time = (time.time() + duration) if duration is not None else 0

        callback = self._get_scanning_callback(matches_map)
        self._scanner.register(callback)

        while not (first and matches_map) and \
                (not stop_time or time.time() < stop_time):
            time.sleep(0.1)

        self._scanner.unregister(callback)

        matches = list(matches_map.values())
        matches.sort(key=lambda x: -x['supplement']['advertisement'].rssi)

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
        self._rebuild_data()
        self._connected = True

        return self

    def disconnect(self):
        self._connected = False
        self._rebuild_data()

        return self

    # -- Data sending --------------------------------------------------------

    def _rebuild_data(self):
        data = self._magic + [self._connection_state] + self._H + self._R \
            + self._M + self._Z

        checksum = 0xe9
        for b in data:
            checksum ^= b
        data += [checksum]

        self._set_manufacturer_data(data)

    # -- Utilities -----------------------------------------------------------

    def __str__(self):
        s = bytes_to_hex_string([self._connection_state])
        h = bytes_to_hex_string(self._H)
        r = bytes_to_hex_string(self._R)
        m = bytes_to_hex_string(self._M, connector=',')
        connected = 'connected' if (self._connected) else 'unconnected'
        return f'{self.__class__.__name__}({connected}, '\
            f'state: {s}, h: {h}, r: {r}, h: {h}, m: {m})'
