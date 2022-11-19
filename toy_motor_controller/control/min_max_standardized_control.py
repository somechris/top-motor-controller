# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import StandardizedControl


class MinMaxStandardizedControl(StandardizedControl):
    def __init__(self, setter, initial_value=0, min=0, max=100):
        super().__init__(setter, initial_value)

        self._min = min
        self._span = max - min

    def _convert_reported_to_backend_value(self, value):
        return self._min + ((value + 100) * self._span) / 200
