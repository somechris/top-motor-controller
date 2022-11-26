# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import patch

from toy_motor_controller.bus.dbus import InvalidArgsException
from toy_motor_controller.bus.dbus import PropertiesObject

from tests import BasicTestCase


class PropertiesObjectTestCase(BasicTestCase):
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_enlist_as_managed_property_object_empty(self, init):
        obj = self.PropertiesObjectStub('/quux', 'iface-FOO', {'foo': 'bar'})

        actual = {}
        obj.enlist_as_managed_property_object(actual)

        self.assertEqual(actual, {
                '/quux': {
                    'iface-FOO': {
                        'foo': 'bar'
                        },
                    },
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_enlist_as_managed_property_object_non_empty(self, init):
        obj = self.PropertiesObjectStub('/quux', 'iface-FOO', {'foo': 'bar'})

        actual = {'FOO': 'BAR'}
        obj.enlist_as_managed_property_object(actual)

        self.assertEqual(actual, {
                '/quux': {
                    'iface-FOO': {
                        'foo': 'bar'
                        },
                    },
                'FOO': 'BAR',
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_GetAll_plain(self, init):
        obj = self.PropertiesObjectStub('/quux', 'iface-FOO', {'foo': 'bar'})

        actual = obj.GetAll('iface-FOO')

        self.assertEqual(actual, {'foo': 'bar'})

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_GetAll_wrong_interface(self, init):
        obj = self.PropertiesObjectStub('/quux', 'iface-FOO', {'foo': 'bar'})

        with self.assertRaises(InvalidArgsException):
            obj.GetAll('foo')

    class PropertiesObjectStub(PropertiesObject):
        def __init__(self, path, interface, properties):
            super().__init__(interface)
            self._properties = properties
            self._object_path = path

        def _get_main_interface_properties(self):
            return self._properties
