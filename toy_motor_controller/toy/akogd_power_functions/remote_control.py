# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.control import uint8_standardized_control
from toy_motor_controller.util import randombyte, bytes_to_hex_string, \
    hex_string_to_bytes

from . import AkogdPowerFunctionsDevice


class AkogdPowerFunctionsRemoteControl(AkogdPowerFunctionsDevice):

    # -- Initialization ------------------------------------------------------

    def __init__(self):
        super().__init__()
        self._connection_state = 1
        self._R = [randombyte() for i in range(3)]
        self._rebuild_data()
        self.advertise()

    # -- Connection handling -------------------------------------------------

    def _get_scanning_callback(self, matches_map):
        needle = bytes_to_hex_string(self._R)

        def callback(advertisement):
            m = advertisement.data.get('Manufacturer', '')
            if len(m) == 42 and m.startswith(self._magic_str + '05'):
                # It's a hub wanting to sync with some remote controller
                if m[14:].startswith(needle):
                    # It's a hub wanting to sync with us \o/
                    H = hex_string_to_bytes(m[8:14])
                    matches_map[advertisement.address] = {
                        'H': H,
                        'supplement': {
                            'advertisement': advertisement,
                            'key': -advertisement.rssi,
                            }
                        }
        return callback

    def connect(self, H):
        self._connection_state = 2
        self._H = H
        self._M = [0x80 for i in range(4)]

        return super().connect()

    def disconnect(self):
        self._connection_state = 1
        self._H = [0 for i in range(3)]
        self._M = [0 for i in range(4)]
        self._rebuild_data()

        return super().disconnect()

    # -- Raw setter ----------------------------------------------------------

    def _set_port(self, port, value):
        self._M[port] = value
        self._rebuild_data()

    # -- User setter ---------------------------------------------------------

    @uint8_standardized_control(
        'Port A (0=full speed counter-clockwise, 100=full speed clockwise)')
    def A(self, value):
        self._set_port(0, value)

    @uint8_standardized_control(
        'Port B (0=full speed counter-clockwise, 100=full speed clockwise)')
    def B(self, value):
        self._set_port(1, value)

    @uint8_standardized_control(
        'Port C (0=full speed counter-clockwise, 100=full speed clockwise)')
    def C(self, value):
        self._set_port(2, value)

    @uint8_standardized_control(
        'Port D (0=full speed counter-clockwise, 100=full speed clockwise)')
    def D(self, value):
        self._set_port(3, value)
