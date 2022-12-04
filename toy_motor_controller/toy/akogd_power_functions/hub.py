# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.util import randombyte, bytes_to_hex_string, \
    hex_string_to_bytes

from . import AkogdPowerFunctionsDevice


class AkogdPowerFunctionsHub(AkogdPowerFunctionsDevice):

    # -- Initialization ------------------------------------------------------

    def __init__(self):
        super().__init__()
        self._H = [randombyte() for i in range(3)]
        self._M[0] = 0x80
        self._rebuild_data()

        self._reset_state()
        self._state_change_listeners = []

    # -- Connection handling -------------------------------------------------
    def _get_scanning_callback(self, matches_map):
        required_start = self._magic_str + '0'
        required_continuations = ['1000000', '3000000']

        def callback(advertisement):
            m = advertisement.data.get('Manufacturer', '')
            if len(m) == 42 and m.startswith(required_start):
                if m[7:14] in required_continuations:
                    # It's an unpeered remote control.
                    R = hex_string_to_bytes(m[14:20])
                    matches_map[advertisement.address] = {
                        'R': R,
                        'supplement': {
                            'advertisement': advertisement,
                            'key': -advertisement.rssi,
                            }
                        }
        return callback

    def connect(self, R):
        self._connection_state = 5
        self._R = R
        self._reset_state()

        super().connect()

        self._expected_advertisement_starts = [
            bytes_to_hex_string(self._magic + [0x02] + self._H + self._R),
            bytes_to_hex_string(self._magic + [0x04] + self._H + self._R),
            ]
        self._expected_advertisement_start = None

        self._scanner.register(self._connected_scan_callback)

        self.advertise()

        return self

    def disconnect(self):
        self._scanner.unregister(self._connected_scan_callback)

        self._connection_state = 0
        self._R = [0 for i in range(3)]
        self._reset_state()

        return super().disconnect()

    # -- Data handling -------------------------------------------------------

    def _reset_state(self):
        self._raw_scanned_state = '80808080'
        self._state = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

    def _connected_scan_callback(self, advertisement):
        m = advertisement.data.get('Manufacturer', '')
        advertisement_start = m[0:20]
        if advertisement_start in self._expected_advertisement_starts:
            self.unadvertise()
            raw_scanned_state = m[20:28]
            if self._raw_scanned_state != raw_scanned_state:
                self._raw_scanned_state = raw_scanned_state
                self._process_raw_scanned_state_change(raw_scanned_state)

    def _process_raw_scanned_state_change(self, raw_scanned_state):
        parsed = hex_string_to_bytes(raw_scanned_state)
        state = {}
        mapping = ['A', 'B', 'C', 'D']
        for i in range(4):
            state[mapping[i]] = - 100 + int(parsed[i] * 200 / 255)

        old_state = self._state
        self._state = state

        for listener in self._state_change_listeners:
            listener(state=state, old_state=old_state)

    def register_state_change(self, callback):
        self._state_change_listeners.append(callback)

    def unregister_state_change(self, callback):
        self._state_change_listeners.remove(callback)
