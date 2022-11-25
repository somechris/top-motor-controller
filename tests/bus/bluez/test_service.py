# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus

from unittest.mock import patch, Mock

from toy_motor_controller.bus.dbus import InvalidArgsException
from toy_motor_controller.bus.bluez import Service
from toy_motor_controller.bus.bluez import GATT_SERVICE_IFACE

from tests import BasicTestCase


class ServiceTestCase(BasicTestCase):
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_unbound(self, init):
        application = Mock()
        application.add = Mock()

        service = Service('uuid-foo')
        service.bind(application)

        application.add.assert_called_once_with(service)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_bound_same(self, init):
        application = Mock()
        application.add = Mock()

        service = Service('uuid-foo')
        service.bind(application)
        service.bind(application)

        application.add.assert_called_once_with(service)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_bound_different(self, init):
        applicationA = Mock()
        applicationA.add = Mock()
        applicationA.remove = Mock()

        applicationB = Mock()
        applicationB.add = Mock()

        service = Service('uuid-foo')
        service.bind(applicationA)
        service.bind(applicationB)

        applicationA.add.assert_called_once_with(service)
        applicationA.remove.assert_called_once_with(service)

        applicationB.add.assert_called_once_with(service)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_unbind_unbound(self, init):
        service = Service('uuid-foo')

        service.unbind()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_unbind_bound(self, init):
        application = Mock()
        application.add = Mock()
        application.remove = Mock()

        service = Service('uuid-foo')
        service.bind(application)
        service.unbind()

        application.add.assert_called_once_with(service)
        application.remove.assert_called_once_with(service)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_single(self, init):
        characteristic = Mock()
        characteristic.bind = Mock()
        characteristic.unbind = Mock()

        service = Service('uuid-foo')
        service.add(characteristic)

        characteristic.bind.assert_called_once_with(service)
        characteristic.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_multiple(self, init):
        characteristic1 = Mock()
        characteristic1.bind = Mock()
        characteristic1.unbind = Mock()

        characteristic2 = Mock()
        characteristic2.bind = Mock()
        characteristic2.unbind = Mock()

        service = Service('uuid-foo')
        service.add(characteristic1)
        service.add(characteristic2)

        characteristic1.bind.assert_called_once_with(service)
        characteristic1.unbind.assert_not_called()

        characteristic2.bind.assert_called_once_with(service)
        characteristic2.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_same_twice(self, init):
        characteristic = Mock()
        characteristic.bind = Mock()
        characteristic.unbind = Mock()

        service = Service('uuid-foo')
        service.add(characteristic)
        service.add(characteristic)

        characteristic.bind.assert_called_once_with(service)
        characteristic.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_remove_not_added(self, init):
        characteristic = Mock()
        characteristic.bind = Mock()
        characteristic.unbind = Mock()

        service = Service('uuid-foo')
        service.remove(characteristic)

        characteristic.bind.assert_not_called()
        characteristic.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_remove_plain(self, init):
        characteristic = Mock()
        characteristic.bind = Mock()
        characteristic.unbind = Mock()

        service = Service('uuid-foo')
        service.add(characteristic)
        service.remove(characteristic)

        characteristic.bind.assert_called_once_with(service)
        characteristic.unbind.assert_called_once_with()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_primary(self, init):
        service = Service('uuid-foo', True)

        actual = service.GetAll(GATT_SERVICE_IFACE)

        self.assertEqual(actual, {
                'UUID': 'uuid-foo',
                'Primary': True,
                'Characteristics': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_single_characteristic(self, init):
        service = Service('uuid-foo', False)

        characteristic = Mock()
        characteristic.dbus_path = '/path/baz'
        service.add(characteristic)

        actual = service.GetAll(GATT_SERVICE_IFACE)

        self.assertEqual(actual, {
                'UUID': 'uuid-foo',
                'Primary': False,
                'Characteristics': dbus.Array([
                        dbus.ObjectPath('/path/baz'),
                        ], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_multiple_characteristics(self, init):
        service = Service('uuid-foo', False)

        characteristic1 = Mock()
        characteristic1.dbus_path = '/path/baz'
        service.add(characteristic1)

        characteristic2 = Mock()
        characteristic2.dbus_path = '/path/quux'
        service.add(characteristic2)

        actual = service.GetAll(GATT_SERVICE_IFACE)

        self.assertEqual(actual, {
                'UUID': 'uuid-foo',
                'Primary': False,
                'Characteristics': dbus.Array([
                        dbus.ObjectPath('/path/baz'),
                        dbus.ObjectPath('/path/quux'),
                        ], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_wrong_interface(self, init):
        service = Service('uuid-foo')

        with self.assertRaises(InvalidArgsException):
            service.GetAll('foo')

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_enlist_as_managed_property_object_no_characteristics(self, init):
        service = Service('uuid-foo', True)
        service._object_path = '/path/foo'

        actual = {}
        service.enlist_as_managed_property_object(actual)

        self.assertEqual(actual, {
                '/path/foo': {
                    'org.bluez.GattService1': {
                        'UUID': 'uuid-foo',
                        'Primary': True,
                        'Characteristics': dbus.Array(
                            [], signature=dbus.Signature('o'))},
                    },
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_enlist_as_managed_property_object_single_characteristics(
            self, init):
        service = Service('uuid-foo', True)
        service._object_path = '/path/foo'

        def characteristic1enlister(obj):
            obj['/path/baz1'] = 'baz1'
        characteristic1 = Mock()
        characteristic1.dbus_path = '/path/bar'
        characteristic1.enlist_as_managed_property_object = \
            characteristic1enlister
        service.add(characteristic1)

        actual = {}
        service.enlist_as_managed_property_object(actual)

        self.assertEqual(actual, {
                '/path/foo': {
                    'org.bluez.GattService1': {
                        'UUID': 'uuid-foo',
                        'Primary': True,
                        'Characteristics': dbus.Array([
                                dbus.ObjectPath('/path/bar'),
                                ], signature=dbus.Signature('o')),
                        },
                    },
                '/path/baz1': 'baz1',
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_enlist_as_managed_property_object_multiple_characteristics(
            self, init):
        service = Service('uuid-foo', True)
        service._object_path = '/path/foo'

        def characteristic1enlister(obj):
            obj['/path/baz1'] = 'baz1'
        characteristic1 = Mock()
        characteristic1.dbus_path = '/path/bar'
        characteristic1.enlist_as_managed_property_object = \
            characteristic1enlister
        service.add(characteristic1)

        def characteristic2enlister(obj):
            obj['/path/baz2'] = 'baz2'
        characteristic2 = Mock()
        characteristic2.dbus_path = '/path/baz'
        characteristic2.enlist_as_managed_property_object = \
            characteristic2enlister
        service.add(characteristic2)

        actual = {}
        service.enlist_as_managed_property_object(actual)

        self.assertEqual(actual, {
                '/path/foo': {
                    'org.bluez.GattService1': {
                        'UUID': 'uuid-foo',
                        'Primary': True,
                        'Characteristics': dbus.Array([
                                dbus.ObjectPath('/path/bar'),
                                dbus.ObjectPath('/path/baz'),
                                ], signature=dbus.Signature('o')),
                        },
                    },
                '/path/baz1': 'baz1',
                '/path/baz2': 'baz2',
                })
