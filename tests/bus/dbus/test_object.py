# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import patch, Mock

from toy_motor_controller.bus.dbus import Object

from tests import BasicTestCase


class ObjectTestCase(BasicTestCase):
    @patch('toy_motor_controller.bus.dbus.get_dbus')
    @patch('toy_motor_controller.bus.dbus.get_dbus_object_registry')
    def test_dbus_path_single(self, object_registry_getter, dbus_getter):
        dbus = Mock()
        dbus_getter.return_value = dbus

        object_registry = Mock()
        object_registry.create_path = Mock(return_value='/FOO')
        object_registry_getter.return_value = object_registry

        obj = Object()

        object_registry.create_path.assert_called_once_with(obj)

        self.assertEqual(obj.dbus_path, '/FOO')
