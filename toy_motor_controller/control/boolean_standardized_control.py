# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import StandardizedControl


class BooleanStandardizedControl(StandardizedControl):
    def _convert_reported_to_backend_value(self, value):
        return value >= 50
