# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.bus.bluez import get_scanner

from . import DiscoveryBase


class BluetoothAdvertisementDiscovery(DiscoveryBase):
    # -- Initialization ------------------------------------------------------

    def __init__(self, **kwargs):
        self._scanner = get_scanner()

        super().__init__(**kwargs)

    # -- Scanning ------------------------------------------------------------

    def _get_scanning_callback(self, matches_map):
        raise NotImplementedError()

    def _start_scan(self, matches_map):
        callback = self._get_scanning_callback(matches_map)
        self._scanner.register(callback)

        return {'callback': callback}

    def _stop_scan(self, scan_state):
        self._scanner.unregister(scan_state['callback'])
