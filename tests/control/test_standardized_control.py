# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import Mock

from toy_motor_controller.control import StandardizedControl

from ..environment import BasicTestCase


class StandardizedControlTestCase(BasicTestCase):
    def test_unintialized_get(self):
        setter = Mock()

        control = StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)
        setter.assert_not_called()

    def test_intial_value_valid_get(self):
        setter = Mock()

        control = StandardizedControl(setter, initial_value=42)

        self.assertEqual(control.get(None), 42)
        setter.assert_not_called()

    def test_intial_value_negative_get(self):
        setter = Mock()

        control = StandardizedControl(setter, initial_value=-42)

        self.assertEqual(control.get(None), -42)
        setter.assert_not_called()

    def test_intial_value_too_low_get(self):
        setter = Mock()

        control = StandardizedControl(setter, initial_value=-142)

        self.assertEqual(control.get(None), -100)
        setter.assert_not_called()

    def test_intial_value_too_high_get(self):
        setter = Mock()

        control = StandardizedControl(setter, initial_value=110)

        self.assertEqual(control.get(None), 100)
        setter.assert_not_called()

    def test_intial_value_true_get(self):
        setter = Mock()

        control = StandardizedControl(setter, initial_value=True)

        self.assertEqual(control.get(None), 100)
        setter.assert_not_called()

    def test_intial_value_false_get(self):
        setter = Mock()

        control = StandardizedControl(setter, initial_value=False)

        self.assertEqual(control.get(None), 0)
        setter.assert_not_called()

    def test_set_once(self):
        setter = Mock()

        control = StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 42)

        setter.assert_called_once_with(None, 42)
        self.assertEqual(control.get(None), 42)

    def test_set_once_negative(self):
        setter = Mock()

        control = StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, -10)

        setter.assert_called_once_with(None, -10)
        self.assertEqual(control.get(None), -10)

    def test_set_once_above(self):
        setter = Mock()

        control = StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 111)

        setter.assert_called_once_with(None, 100)
        self.assertEqual(control.get(None), 100)

    def test_set_once_below(self):
        setter = Mock()

        control = StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, -120)

        setter.assert_called_once_with(None, -100)
        self.assertEqual(control.get(None), -100)

    def test_set_multiple_times(self):
        setter = Mock()

        control = StandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 42)
        setter.assert_called_once_with(None, 42)
        setter.reset_mock()
        self.assertEqual(control.get(None), 42)

        control.set(None, -10)
        setter.assert_called_once_with(None, -10)
        setter.reset_mock()
        self.assertEqual(control.get(None), -10)

        control.set(None, 50)
        setter.assert_called_once_with(None, 50)
        setter.reset_mock()
        self.assertEqual(control.get(None), 50)
