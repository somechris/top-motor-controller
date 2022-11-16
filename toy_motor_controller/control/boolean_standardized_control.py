# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import StandardizedControl


class BooleanStandardizedControl(StandardizedControl):
    def _convert_to_reported_value(self, value):
        value = super(BooleanStandardizedControl, self)\
            ._convert_to_reported_value(value)

        return 100 if value >= 50 else 0

    def _convert_reported_to_backend_value(self, value):
        return value >= 50
