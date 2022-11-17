# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import Control

from toy_motor_controller.util import clamped


class StandardizedControl(Control):
    def __init__(self, setter, initial_value=0):
        super(StandardizedControl, self).__init__(setter, initial_value)

    def _convert_to_reported_value(self, value):
        value = super(StandardizedControl, self)\
            ._convert_to_reported_value(value)

        if value is True:
            value = 100
        elif value is False:
            value = 0

        value = clamped(value, -100, 100)

        return value
