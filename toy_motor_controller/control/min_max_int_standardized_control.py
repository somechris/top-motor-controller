# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import MinMaxStandardizedControl


class MinMaxIntStandardizedControl(MinMaxStandardizedControl):
    def __init__(self, setter, initial_value=None, min=0, max=100):
        super(MinMaxIntStandardizedControl, self).__init__(
            setter, initial_value, min, max)

    def _coerce_standardized_value(self, value):
        value = super(MinMaxIntStandardizedControl, self)\
            ._coerce_standardized_value(value)
        return int(value + 0.5)
