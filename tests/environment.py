# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import unittest


class BasicTestCase(unittest.TestCase):
    def assertMinMax(self, value, minimum, maximum):
        self.assertLessEqual(minimum, value)
        self.assertLessEqual(value, maximum)
