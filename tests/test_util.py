# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .environment import BasicTestCase

from toy_motor_controller.util import \
    randombyte, \
    bytes_to_hex_string, \
    clamped, \
    clamped_int


class ControlTestCase(BasicTestCase):
    def test_random_byte(self):
        actual = randombyte()
        self.assertMinMax(actual, 0, 255)

    def test_random_byte_crude_randomness(self):
        numbers = [randombyte() for _ in range(20)]
        self.assertGreater(len(numbers), 15)

    def test_bytes_to_hex_string_empty(self):
        actual = bytes_to_hex_string([])
        self.assertEqual(actual, '')

    def test_bytes_to_hex_string_single_small(self):
        actual = bytes_to_hex_string([0xc])
        self.assertEqual(actual, '0c')

    def test_bytes_to_hex_string_single_big(self):
        actual = bytes_to_hex_string([0xfa])
        self.assertEqual(actual, 'fa')

    def test_bytes_to_hex_string_multiple(self):
        actual = bytes_to_hex_string([0xf0, 0x0b, 0xa4])
        self.assertEqual(actual, 'f00ba4')

    def test_bytes_to_hex_string_multiple_connector(self):
        actual = bytes_to_hex_string([0xf0, 0x0b, 0xa4], connector='__')
        self.assertEqual(actual, 'f0__0b__a4')

    def test_clamped_between(self):
        actual = clamped(30.5, 10.4, 87)
        self.assertEqual(actual, 30.5)

    def test_clamped_below(self):
        actual = clamped(0.5, 10.4, 87)
        self.assertEqual(actual, 10.4)

    def test_clamped_above(self):
        actual = clamped(100, 10.4, 87)
        self.assertEqual(actual, 87)

    def test_clamped_int_between_round_down(self):
        actual = clamped_int(30.4, 10, 87)
        self.assertEqual(actual, 30)

    def test_clamped_int_between_round_up(self):
        actual = clamped_int(30.6, 10, 87)
        self.assertEqual(actual, 31)

    def test_clamped_int_below(self):
        actual = clamped_int(0.5, 10, 87)
        self.assertEqual(actual, 10)

    def test_clamped_int_above(self):
        actual = clamped_int(100, 10, 87)
        self.assertEqual(actual, 87)
