# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.bus.bluez import Characteristic
from toy_motor_controller.control import boolean_standardized_control
from toy_motor_controller.control import min_max_int_standardized_control
from toy_motor_controller.control import resending_control
from toy_motor_controller.control import uint8_standardized_control
from toy_motor_controller.util import clamped_int

import logging
logger = logging.getLogger(__name__)


class PlaymobilRacerRemoteControl(object):
    CHARACTERISTIC_UUID = '06d1e5e7-79ad-4a71-8faa-373789f7d93c'

    # -- Initialization ------------------------------------------------------

    def __init__(self):
        self._remote_addr = None
        self._characteristic = None

    # -- Connection handling -------------------------------------------------

    def connect(self, addr):
        self._remote_addr = addr
        self._characteristic = Characteristic(
            self._remote_addr, self.CHARACTERISTIC_UUID)

    # -- Data sending --------------------------------------------------------

    def _send_command(self, key, value):
        data = bytes([key, value, 0x0f])
        logger.debug('Writing command '
                     f'{data[0]:02x} {data[1]:02x} {data[2]:02x}')
        self._characteristic.write(data)

    # -- Raw setter ----------------------------------------------------------

    def _set_speed_motor(self, value):
        self._send_command(0x23, value)

    def _set_light(self, value):
        self._send_command(0x24, 2 if value else 1)

    def _set_speed_multiplier(self, value):
        self._send_command(0x25, clamped_int(value, 1, 5))

    def _set_steering_motor(self, value):
        self._send_command(0x40, value)

    # -- User setter ---------------------------------------------------------

    @uint8_standardized_control(
        'Speed (0=full speed backwards, 100=full speed forwards)')
    # Set value holds only for ~0.3 seconds, so we need to resend before that.
    @resending_control(interval=0.20)
    def speed(self, value):
        self._set_speed_motor(value)

    @boolean_standardized_control('Light (True=lights on, False=lights off)')
    def light(self, value):
        self._set_light(value)

    @min_max_int_standardized_control('Speed multiplyer (0=slow, 100=fast)',
                                      min=1, max=5)
    def speed_multiplier(self, value):
        self._set_speed_multiplier(value)

    @uint8_standardized_control('Steering direction (0=left, 100=right)')
    def direction(self, value):
        self._set_steering_motor(value)

    # -- Utilities -----------------------------------------------------------

    def __str__(self):
        if self._remote_addr:
            extra = self._remote_addr
        else:
            extra = '<unconnected>'
        return f'PlaymobilRacerRemoteControl({extra})'
