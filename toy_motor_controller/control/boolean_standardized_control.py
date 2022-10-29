# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import StandardizedControl


class BooleanStandardizedControl(StandardizedControl):
    def _coerce_standardized_value(self, value):
        return value >= 50
