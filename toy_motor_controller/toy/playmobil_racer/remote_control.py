# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.bus.bluez import Characteristic
from toy_motor_controller.util import clamped_int

import logging
logger = logging.getLogger(__name__)


class PlaymobilRacerRemoteControl(object):
    CHARACTERISTIC_UUID = '06d1e5e7-79ad-4a71-8faa-373789f7d93c'

    def __init__(self):
        self._remote_addr = None
        self._characteristic = None

    def connected(self, addr):
        self._remote_addr = addr
        self._characteristic = Characteristic(
            self._remote_addr, self.CHARACTERISTIC_UUID)

    def _send_command(self, key, value):
        data = bytes([key, value, 0x0f])
        logger.debug('Writing command '
                     f'{data[0]:02x} {data[1]:02x} {data[2]:02x}')
        self._characteristic.write(data)

    def _set_speed_motor(self, value):
        self._send_command(0x23, value)

    def _set_light(self, value):
        self._send_command(0x24, 2 if value else 1)

    def _set_speed_multiplier(self, value):
        self._send_command(0x25, clamped_int(value, 1, 5))

    def _set_steering_motor(self, value):
        self._send_command(0x40, value)

    def __str__(self):
        if self._remote_addr:
            extra = self._remote_addr
        else:
            extra = '<unconnected>'
        return f'PlaymobilRacerRemoteControl({extra})'
