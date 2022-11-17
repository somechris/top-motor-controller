# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import Mock

from toy_motor_controller.control import BooleanStandardizedControl

from ..environment import BasicTestCase


class BooleanStandardizedControlTXstCase(BasicTestCase):
    def test_unintialized_get(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter)

        self.assertEqual(control.get(None), 0)
        setter.assert_not_called()

    def test_intial_value_valid_get(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter, initial_value=True)

        self.assertEqual(control.get(None), 100)
        setter.assert_not_called()

    def test_intial_value_low_number(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter, initial_value=-5)

        self.assertEqual(control.get(None), -5)
        setter.assert_not_called()

    def test_intial_value_high_number(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter, initial_value=67)

        self.assertEqual(control.get(None), 67)
        setter.assert_not_called()

    def test_set_once(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, True)

        setter.assert_called_once_with(None, True)
        self.assertEqual(control.get(None), 100)

    def test_set_once_low_number(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 45)

        setter.assert_called_once_with(None, False)
        self.assertEqual(control.get(None), 45)

    def test_set_once_high_number(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, 55)

        setter.assert_called_once_with(None, True)
        self.assertEqual(control.get(None), 55)

    def test_set_once_negative_number(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, -70)

        setter.assert_called_once_with(None, False)
        self.assertEqual(control.get(None), -70)

    def test_set_multiple_times(self):
        setter = Mock()

        control = BooleanStandardizedControl(setter)

        self.assertEqual(control.get(None), 0)

        control.set(None, True)

        setter.assert_called_once_with(None, True)
        setter.reset_mock()
        self.assertEqual(control.get(None), 100)

        control.set(None, False)
        setter.assert_called_once_with(None, False)
        setter.reset_mock()
        self.assertEqual(control.get(None), 0)

        control.set(None, True)
        setter.assert_called_once_with(None, True)
        setter.reset_mock()
        self.assertEqual(control.get(None), 100)

        control.set(None, 40)
        setter.assert_called_once_with(None, False)
        setter.reset_mock()
        self.assertEqual(control.get(None), 40)

        control.set(None, 60)
        setter.assert_called_once_with(None, True)
        setter.reset_mock()
        self.assertEqual(control.get(None), 60)
