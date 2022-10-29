# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import StandardizedControl


class MinMaxStandardizedControl(StandardizedControl):
    def __init__(self, setter, initial_value=None, min=0, max=100):
        self._min = min
        self._span = max - min
        super(MinMaxStandardizedControl, self).__init__(setter, initial_value)

    def _coerce_standardized_value(self, value):
        return self._min + (value * self._span) / 100
