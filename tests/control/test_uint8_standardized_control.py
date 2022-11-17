# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import Mock

from toy_motor_controller.control import UInt8StandardizedControl

from ..environment import BasicTestCase


class UInt8StandardizedControlTestCase(BasicTestCase):
    def test_unintialized_get(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)
        setter.assert_not_called()

    def test_intial_value_valid_get(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter, initial_value=42)

        self.assertEqual(control.get(None), 42)
        setter.assert_not_called()

    def test_intial_value_valid_negative_get(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter, initial_value=-42)

        self.assertEqual(control.get(None), -42)
        setter.assert_not_called()

    def test_intial_value_too_low_get(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter, initial_value=-210)

        self.assertEqual(control.get(None), -100)
        setter.assert_not_called()

    def test_intial_value_too_high_get(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter, initial_value=110)

        self.assertEqual(control.get(None), 100)
        setter.assert_not_called()

    def test_set_once_middle(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 0)

        setter.assert_called_once_with(None, 128)
        self.assertEqual(control.get(None), 0)

    def test_set_once_round_down(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 73)

        setter.assert_called_once_with(None, 221)
        self.assertEqual(control.get(None), 73)

    def test_set_once_round_up(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 74)

        setter.assert_called_once_with(None, 222)
        self.assertEqual(control.get(None), 74)

    def test_set_once_too_low_number(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, -210)

        setter.assert_called_once_with(None, 0)
        self.assertEqual(control.get(None), -100)

    def test_set_once_too_high_number(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 110)

        setter.assert_called_once_with(None, 255)
        self.assertEqual(control.get(None), 100)

    def test_set_multiple_times(self):
        setter = Mock()

        control = UInt8StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, True)

        setter.assert_called_once_with(None, 255)
        setter.reset_mock()
        self.assertEqual(control.get(None), 100)

        control.set(None, 10)
        setter.assert_called_once_with(None, 140)
        setter.reset_mock()
        self.assertEqual(control.get(None), 10)

        control.set(None, -20)
        setter.assert_called_once_with(None, 102)
        setter.reset_mock()
        self.assertEqual(control.get(None), -20)
