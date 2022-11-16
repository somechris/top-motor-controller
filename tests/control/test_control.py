# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import Mock

from toy_motor_controller.control import Control

from ..environment import BasicTestCase


class ControlTestCase(BasicTestCase):
    def test_unintialized_get(self):
        setter = Mock()

        control = Control(setter)

        self.assertEqual(control.get(None), None)
        setter.assert_not_called()

    def test_intial_value_get(self):
        setter = Mock()

        control = Control(setter, initial_value=42)

        self.assertEqual(control.get(None), 42)
        setter.assert_not_called()

    def test_set_once(self):
        setter = Mock()

        control = Control(setter)

        self.assertEqual(control.get(None), None)

        control.set(None, 42)

        setter.assert_called_once_with(None, 42)
        self.assertEqual(control.get(None), 42)

    def test_set_multiple_times(self):
        setter = Mock()

        control = Control(setter, initial_value=4711)

        self.assertEqual(control.get(None), 4711)

        control.set(None, 42)

        setter.assert_called_once_with(None, 42)
        setter.reset_mock()
        self.assertEqual(control.get(None), 42)

        control.set(None, 23)
        setter.assert_called_once_with(None, 23)
        setter.reset_mock()
        self.assertEqual(control.get(None), 23)

        control.set(None, 17)
        setter.assert_called_once_with(None, 17)
        setter.reset_mock()
        self.assertEqual(control.get(None), 17)
