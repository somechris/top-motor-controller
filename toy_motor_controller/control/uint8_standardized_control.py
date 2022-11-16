# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import MinMaxIntStandardizedControl


class UInt8StandardizedControl(MinMaxIntStandardizedControl):
    def __init__(self, setter, initial_value=0):
        super(UInt8StandardizedControl, self).__init__(
            setter, initial_value, min=0, max=255)
