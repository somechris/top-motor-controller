# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from tests import BasicTestCase

from toy_motor_controller.util import randombyte
from toy_motor_controller.util import bytes_to_hex_string
from toy_motor_controller.util import hex_string_to_bytes
from toy_motor_controller.util import clamped
from toy_motor_controller.util import clamped_int
from toy_motor_controller.util import get_fully_qualified_class_name
from toy_motor_controller.util import get_fully_qualified_inherited_class_names
from toy_motor_controller.util import get_fully_qualified_inherited_names
from toy_motor_controller.util import get_fully_qualified_name
from toy_motor_controller.util import normalize_mac_address


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

    def test_hex_string_to_bytes_empty(self):
        actual = hex_string_to_bytes('')
        self.assertEqual(actual, [])

    def test_hex_string_to_bytes_single_char_low(self):
        actual = hex_string_to_bytes('5')
        self.assertEqual(actual, [0x05])

    def test_hex_string_to_bytes_single_char_high(self):
        actual = hex_string_to_bytes('e')
        self.assertEqual(actual, [0x0e])

    def test_hex_string_to_bytes_single_byte(self):
        actual = hex_string_to_bytes('a8')
        self.assertEqual(actual, [0xa8])

    def test_hex_string_to_bytes_multiple_bytes(self):
        actual = hex_string_to_bytes('a84011')
        self.assertEqual(actual, [0xa8, 0x40, 0x11])

    def test_hex_string_to_bytes_multiple_bytes_uneven(self):
        actual = hex_string_to_bytes('a840113')
        self.assertEqual(actual, [0x0a, 0x84, 0x01, 0x13])

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

    def test_get_fully_qualified_name_None(self):
        actual = get_fully_qualified_name(None.__class__)
        self.assertEqual(actual, 'builtins.NoneType')

    def test_get_fully_qualified_name_object(self):
        actual = get_fully_qualified_name(object().__class__)
        self.assertEqual(actual, 'builtins.object')

    def test_get_fully_qualified_name_string(self):
        actual = get_fully_qualified_name('foo'.__class__)
        self.assertEqual(actual, 'builtins.str')

    def test_get_fully_qualified_name_self(self):
        actual = get_fully_qualified_name(self.__class__)
        self.assertEqual(actual, 'tests.test_util.ControlTestCase')

    def test_get_fully_qualified_name_self_ABBCD(self):
        actual = get_fully_qualified_name(self.clsABBCD)
        self.assertEqual(actual, 'tests.test_util.ControlTestCase.clsABBCD')

    def test_get_fully_qualified_class_name_None(self):
        actual = get_fully_qualified_class_name(None)
        self.assertEqual(actual, 'builtins.NoneType')

    def test_get_fully_qualified_class_name_object(self):
        actual = get_fully_qualified_class_name(object())
        self.assertEqual(actual, 'builtins.object')

    def test_get_fully_qualified_class_name_string(self):
        actual = get_fully_qualified_class_name('foo')
        self.assertEqual(actual, 'builtins.str')

    def test_get_fully_qualified_class_name_self(self):
        actual = get_fully_qualified_class_name(self)
        self.assertEqual(actual, 'tests.test_util.ControlTestCase')

    def test_get_fully_qualified_class_name_self_ABBCD(self):
        actual = get_fully_qualified_class_name(self.clsABBCD())
        self.assertEqual(actual, 'tests.test_util.ControlTestCase.clsABBCD')

    def test_get_fully_qualified_inherited_class_names_None(self):
        actual = get_fully_qualified_inherited_class_names(None)
        self.assertEqual(list(actual),
                         ['builtins.NoneType', 'builtins.object'])

    def test_get_fully_qualified_inherited_class_names_object(self):
        actual = get_fully_qualified_inherited_class_names(object())
        self.assertEqual(list(actual), ['builtins.object'])

    def test_get_fully_qualified_inherited_class_names_string(self):
        actual = get_fully_qualified_inherited_class_names('foo')
        self.assertEqual(list(actual),
                         ['builtins.str', 'builtins.object'])

    def test_get_fully_qualified_inherited_class_names_self(self):
        actual = get_fully_qualified_inherited_class_names(self)
        self.assertEqual(list(actual), [
                'tests.test_util.ControlTestCase',
                'tests.environment.BasicTestCase',
                'unittest.case.TestCase',
                'builtins.object',
                ])

    def test_get_fully_qualified_inherited_class_names_self_ABBCD(self):
        actual = get_fully_qualified_inherited_class_names(self.clsABBCD())
        self.assertEqual(list(actual), [
                'tests.test_util.ControlTestCase.clsABBCD',
                'tests.test_util.ControlTestCase.clsAB',
                'tests.test_util.ControlTestCase.clsBC',
                'tests.test_util.ControlTestCase.clsD',
                'tests.test_util.ControlTestCase.clsA',
                'tests.test_util.ControlTestCase.clsB',
                'tests.test_util.ControlTestCase.clsC',
                'builtins.object',
                ])

    def test_get_fully_qualified_inherited_names_None(self):
        actual = get_fully_qualified_inherited_names(None.__class__)
        self.assertEqual(list(actual),
                         ['builtins.NoneType', 'builtins.object'])

    def test_get_fully_qualified_inherited_names_object(self):
        actual = get_fully_qualified_inherited_names(object().__class__)
        self.assertEqual(list(actual), ['builtins.object'])

    def test_get_fully_qualified_inherited_names_string(self):
        actual = get_fully_qualified_inherited_names('foo'.__class__)
        self.assertEqual(list(actual), ['builtins.str', 'builtins.object'])

    def test_get_fully_qualified_inherited_names_self(self):
        actual = get_fully_qualified_inherited_names(self.__class__)
        self.assertEqual(list(actual), [
                'tests.test_util.ControlTestCase',
                'tests.environment.BasicTestCase',
                'unittest.case.TestCase',
                'builtins.object',
                ])

    def test_get_fully_qualified_inherited_names_self_ABBCD(self):
        actual = get_fully_qualified_inherited_names(self.clsABBCD)
        self.assertEqual(list(actual), [
                'tests.test_util.ControlTestCase.clsABBCD',
                'tests.test_util.ControlTestCase.clsAB',
                'tests.test_util.ControlTestCase.clsBC',
                'tests.test_util.ControlTestCase.clsD',
                'tests.test_util.ControlTestCase.clsA',
                'tests.test_util.ControlTestCase.clsB',
                'tests.test_util.ControlTestCase.clsC',
                'builtins.object',
                ])

    def test_normalize_mac_address_None(self):
        actual = normalize_mac_address(None)
        self.assertIsNone(actual)

    def test_normalize_mac_address_empty(self):
        actual = normalize_mac_address('')
        self.assertEqual(actual, '')

    def test_normalize_mac_address_lowercase(self):
        actual = normalize_mac_address('01:ab:23:cd:45:ef')
        self.assertEqual(actual, '01:ab:23:cd:45:ef')

    def test_normalize_mac_address_uppercase(self):
        actual = normalize_mac_address('AB:67:CD:89:EF:01')
        self.assertEqual(actual, 'ab:67:cd:89:ef:01')

    def test_normalize_mac_address_mixed_case(self):
        actual = normalize_mac_address('aB:67:cd:89:EF:01')
        self.assertEqual(actual, 'ab:67:cd:89:ef:01')

    class clsA(object):
        pass

    class clsB(object):
        pass

    class clsC(object):
        pass

    class clsD(object):
        pass

    class clsAB(clsA, clsB):
        pass

    class clsBC(clsB, clsC):
        pass

    class clsABBCD(clsAB, clsBC, clsD):
        pass
