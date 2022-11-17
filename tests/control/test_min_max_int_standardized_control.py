# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import Mock

from toy_motor_controller.control import MinMaxIntStandardizedControl

from ..environment import BasicTestCase


class MinMaxIntStandardizedControlTestCase(BasicTestCase):
    def test_unintialized_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter)

        self.assertEqual(control.get(None), 0)
        setter.assert_not_called()

    def test_unintialized_min_max_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=70, max=90)

        self.assertEqual(control.get(None), 0)
        setter.assert_not_called()

    def test_intial_value_valid_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, initial_value=42)

        self.assertEqual(control.get(None), 42)
        setter.assert_not_called()

    def test_intial_value_negative_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, initial_value=-10)

        self.assertEqual(control.get(None), -10)
        setter.assert_not_called()

    def test_intial_value_too_low_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, initial_value=-210)

        self.assertEqual(control.get(None), -100)
        setter.assert_not_called()

    def test_intial_value_too_high_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, initial_value=110)

        self.assertEqual(control.get(None), 100)
        setter.assert_not_called()

    def test_intial_value_valid_min_max_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(
            setter, initial_value=50, min=70, max=90)

        self.assertEqual(control.get(None), 50)
        setter.assert_not_called()

    def test_intial_value_too_low_min_max_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(
            setter, initial_value=-310, min=70, max=90)

        self.assertEqual(control.get(None), -100)
        setter.assert_not_called()

    def test_intial_value_too_high_min_max_get(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(
            setter, initial_value=105, min=70, max=90)

        self.assertEqual(control.get(None), 100)
        setter.assert_not_called()

    def test_set_once(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=1000, max=3000)

        self.assertEqual(control.get(None), 0)

        control.set(None, 70)

        setter.assert_called_once_with(None, 2700)
        self.assertEqual(control.get(None), 70)

    def test_set_once_min_round_up(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=10.1)

        self.assertEqual(control.get(None), 0)

        control.set(None, -100)

        setter.assert_called_once_with(None, 11)
        self.assertEqual(control.get(None), -100)

    def test_set_once_max_round_down(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, max=10.9)

        self.assertEqual(control.get(None), 0)

        control.set(None, 100)

        setter.assert_called_once_with(None, 10)
        self.assertEqual(control.get(None), 100)

    def test_min_coverage_low_end(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=5, max=6)

        self.assertEqual(control.get(None), 0)

        control.set(None, -100)

        setter.assert_called_once_with(None, 5)
        self.assertEqual(control.get(None), -100)

    def test_min_coverage_high_end(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=5, max=6)

        self.assertEqual(control.get(None), 0)

        control.set(None, -1)

        setter.assert_called_once_with(None, 5)
        self.assertEqual(control.get(None), -1)

    def test_max_coverage_low_end(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=5, max=6)

        self.assertEqual(control.get(None), 0)

        control.set(None, 0)

        setter.assert_called_once_with(None, 6)
        self.assertEqual(control.get(None), 0)

    def test_max_coverage_high_end(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=5, max=6)

        self.assertEqual(control.get(None), 0)

        control.set(None, 100)

        setter.assert_called_once_with(None, 6)
        self.assertEqual(control.get(None), 100)

    def test_set_once_float(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=-10, max=10)

        self.assertEqual(control.get(None), 0)

        control.set(None, 23.4)

        setter.assert_called_once_with(None, 2)
        self.assertEqual(control.get(None), 23.4)

    def test_set_once_too_low_number(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=70, max=90)

        self.assertEqual(control.get(None), 0)

        control.set(None, -120)

        setter.assert_called_once_with(None, 70)
        self.assertEqual(control.get(None), -100)

    def test_set_once_too_high_number(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=70, max=90)

        self.assertEqual(control.get(None), 0)

        control.set(None, 110)

        setter.assert_called_once_with(None, 90)
        self.assertEqual(control.get(None), 100)

    def test_set_multiple_times(self):
        setter = Mock()

        control = MinMaxIntStandardizedControl(setter, min=1000, max=3000)

        self.assertEqual(control.get(None), 0)

        control.set(None, True)

        setter.assert_called_once_with(None, 3000)
        setter.reset_mock()
        self.assertEqual(control.get(None), 100)

        control.set(None, 43)
        setter.assert_called_once_with(None, 2430)
        setter.reset_mock()
        self.assertEqual(control.get(None), 43)

        control.set(None, 5000)
        setter.assert_called_once_with(None, 3000)
        setter.reset_mock()
        self.assertEqual(control.get(None), 100)

        control.set(None, -40)
        setter.assert_called_once_with(None, 1600)
        setter.reset_mock()
        self.assertEqual(control.get(None), -40)

        control.set(None, 60)
        setter.assert_called_once_with(None, 2600)
        setter.reset_mock()
        self.assertEqual(control.get(None), 60)
