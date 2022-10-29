# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import Control

from toy_motor_controller.util import clamped_int


class StandardizedControl(Control):
    def __init__(self, setter, initial_value=None):
        super(StandardizedControl, self).__init__(setter, initial_value)
        self._value = \
            self._coerce_value(initial_value if initial_value else 0)

    def get(self, instance):
        return self._value

    def set(self, instance, value):
        self._value = self._coerce_value(value)
        self._backend_setter(instance, self._value)

    def _coerce_standardized_value(self, value):
        return value

    def _coerce_value(self, value):
        if value is True:
            value = 100
        elif value is False:
            value = 0
        else:
            value = clamped_int(value, 0, 100)
        return self._coerce_standardized_value(value)
