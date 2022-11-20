# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import time

from toy_motor_controller.bus.bluez import get_scanner


class BluetoothAdvertisementDiscovery(object):
    def __init__(self):
        self._connected = False
        self._scanner = get_scanner()

        super().__init__()

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
        self._connected = True

        return self

    def disconnect(self):
        self._connected = False

        return self
