# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from math import floor, ceil
from . import MinMaxStandardizedControl


class MinMaxIntStandardizedControl(MinMaxStandardizedControl):
    def __init__(self, setter, initial_value=0, min=0, max=100):
        self._max = floor(max)
        super().__init__(setter, initial_value, ceil(min), self._max + 1)

    def _convert_reported_to_backend_value(self, value):
        value = super()._convert_reported_to_backend_value(value)
        return min(int(value), self._max)
