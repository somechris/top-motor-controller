# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import Control


class BooleanControl(Control):
    def __init__(self, setter, initial_value=None):
        super(BooleanControl, self).__init__(setter, initial_value)

        self._value = initial_value if initial_value is not None else False

    def _coerce_value(self, value):
        return bool(value)
