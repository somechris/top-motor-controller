# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus

from unittest.mock import patch, Mock

from toy_motor_controller.bus.dbus import InvalidArgsException
from toy_motor_controller.bus.bluez import Characteristic
from toy_motor_controller.bus.bluez import GATT_CHARACTERISTIC_IFACE

from tests import BasicTestCase


class CharacteristicTestCase(BasicTestCase):
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_unbound(self, init):
        service = Mock()
        service.add = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.bind(service)

        service.add.assert_called_once_with(characteristic)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_bound_same(self, init):
        service = Mock()
        service.add = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.bind(service)
        characteristic.bind(service)

        service.add.assert_called_once_with(characteristic)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_bound_different(self, init):
        serviceA = Mock()
        serviceA.add = Mock()
        serviceA.remove = Mock()

        serviceB = Mock()
        serviceB.add = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.bind(serviceA)
        characteristic.bind(serviceB)

        serviceA.add.assert_called_once_with(characteristic)
        serviceA.remove.assert_called_once_with(characteristic)

        serviceB.add.assert_called_once_with(characteristic)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_unbind_unbound(self, init):
        characteristic = Characteristic('uuid-foo')

        characteristic.unbind()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_unbind_bound(self, init):
        service = Mock()
        service.add = Mock()
        service.remove = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.bind(service)
        characteristic.unbind()

        service.add.assert_called_once_with(characteristic)
        service.remove.assert_called_once_with(characteristic)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_single(self, init):
        descriptor = Mock()
        descriptor.bind = Mock()
        descriptor.unbind = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.add(descriptor)

        descriptor.bind.assert_called_once_with(characteristic)
        descriptor.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_multiple(self, init):
        descriptor1 = Mock()
        descriptor1.bind = Mock()
        descriptor1.unbind = Mock()

        descriptor2 = Mock()
        descriptor2.bind = Mock()
        descriptor2.unbind = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.add(descriptor1)
        characteristic.add(descriptor2)

        descriptor1.bind.assert_called_once_with(characteristic)
        descriptor1.unbind.assert_not_called()

        descriptor2.bind.assert_called_once_with(characteristic)
        descriptor2.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_same_twice(self, init):
        descriptor = Mock()
        descriptor.bind = Mock()
        descriptor.unbind = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.add(descriptor)
        characteristic.add(descriptor)

        descriptor.bind.assert_called_once_with(characteristic)
        descriptor.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_remove_not_added(self, init):
        descriptor = Mock()
        descriptor.bind = Mock()
        descriptor.unbind = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.remove(descriptor)

        descriptor.bind.assert_not_called()
        descriptor.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_remove_plain(self, init):
        descriptor = Mock()
        descriptor.bind = Mock()
        descriptor.unbind = Mock()

        characteristic = Characteristic('uuid-foo')
        characteristic.add(descriptor)
        characteristic.remove(descriptor)

        descriptor.bind.assert_called_once_with(characteristic)
        descriptor.unbind.assert_called_once_with()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_default_unbound(self, init):
        characteristic = Characteristic('uuid-foo')

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': None,
                'UUID': 'uuid-foo',
                'Flags': [],
                'Descriptors': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_default_bound(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo')
        characteristic.bind(service)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': [],
                'Descriptors': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_indicate(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo', indicate=True)
        characteristic.bind(service)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['indicate'],
                'Descriptors': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_read(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo', read=True)
        characteristic.bind(service)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['read'],
                'Descriptors': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_write(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo', write=True)
        characteristic.bind(service)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['write'],
                'Descriptors': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_notify(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo', notify=True)
        characteristic.bind(service)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['notify'],
                'Descriptors': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_write_without_response(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic(
            'uuid-foo', write_without_response=True)
        characteristic.bind(service)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['write-without-response'],
                'Descriptors': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_all(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic(
            'uuid-foo', indicate=True, read=True, notify=True, write=True,
            write_without_response=True)
        characteristic.bind(service)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['indicate', 'read', 'notify', 'write',
                          'write-without-response'],
                'Descriptors': dbus.Array([], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_single_decorator(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo')
        characteristic.bind(service)

        descriptor = Mock()
        descriptor.dbus_path = '/path/baz'
        characteristic.add(descriptor)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': [],
                'Descriptors': dbus.Array([
                        dbus.ObjectPath('/path/baz'),
                        ], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_multiple_decorators(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo')
        characteristic.bind(service)

        descriptor1 = Mock()
        descriptor1.dbus_path = '/path/baz1'
        characteristic.add(descriptor1)

        descriptor2 = Mock()
        descriptor2.dbus_path = '/path/baz2'
        characteristic.add(descriptor2)

        actual = characteristic.GetAll(GATT_CHARACTERISTIC_IFACE)

        self.assertEqual(actual, {
                'Service': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': [],
                'Descriptors': dbus.Array([
                        dbus.ObjectPath('/path/baz1'),
                        dbus.ObjectPath('/path/baz2'),
                        ], signature='o'),
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_wrong_interface(self, init):
        characteristic = Characteristic('uuid-foo', read=True)

        with self.assertRaises(InvalidArgsException):
            characteristic.GetAll('foo')

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_enlist_as_managed_property_object_no_decorators(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo')
        characteristic._object_path = '/path/foo'
        characteristic.bind(service)

        actual = {}
        characteristic.enlist_as_managed_property_object(actual)

        self.assertEqual(actual, {
            '/path/foo': {
                'org.bluez.GattCharacteristic1': {
                    'Service': dbus.ObjectPath('/path/bar'),
                    'UUID': 'uuid-foo',
                    'Flags': [],
                    'Descriptors': dbus.Array([],
                                              signature=dbus.Signature('o'))
                    },
                },
            })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_enlist_as_managed_property_object_single_decorator(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo')
        characteristic._object_path = '/path/foo'
        characteristic.bind(service)

        def descriptor1enlister(obj):
            obj['/path/baz1'] = 'baz1'
        descriptor1 = Mock()
        descriptor1.dbus_path = '/path/baz1'
        descriptor1.enlist_as_managed_property_object = descriptor1enlister
        characteristic.add(descriptor1)

        actual = {}
        characteristic.enlist_as_managed_property_object(actual)

        self.assertEqual(actual, {
            '/path/foo': {
                'org.bluez.GattCharacteristic1': {
                    'Service': dbus.ObjectPath('/path/bar'),
                    'UUID': 'uuid-foo',
                    'Flags': [],
                    'Descriptors': dbus.Array([
                            dbus.ObjectPath('/path/baz1'),
                            ], signature=dbus.Signature('o'))
                    },
                },
            '/path/baz1': 'baz1',
            })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_enlist_as_managed_property_object_multiple_decorators(self, init):
        service = Mock()
        service.dbus_path = '/path/bar'

        characteristic = Characteristic('uuid-foo')
        characteristic._object_path = '/path/foo'
        characteristic.bind(service)

        def descriptor1enlister(obj):
            obj['/path/baz1'] = 'baz1'
        descriptor1 = Mock()
        descriptor1.dbus_path = '/path/baz1'
        descriptor1.enlist_as_managed_property_object = descriptor1enlister
        characteristic.add(descriptor1)

        def descriptor2enlister(obj):
            obj['/path/baz2'] = 'baz2'
        descriptor2 = Mock()
        descriptor2.dbus_path = '/path/baz2'
        descriptor2.enlist_as_managed_property_object = descriptor2enlister
        characteristic.add(descriptor2)

        actual = {}
        characteristic.enlist_as_managed_property_object(actual)

        self.assertEqual(actual, {
            '/path/foo': {
                'org.bluez.GattCharacteristic1': {
                    'Service': dbus.ObjectPath('/path/bar'),
                    'UUID': 'uuid-foo',
                    'Flags': [],
                    'Descriptors': dbus.Array([
                            dbus.ObjectPath('/path/baz1'),
                            dbus.ObjectPath('/path/baz2')],
                                              signature=dbus.Signature('o'))
                    },
                },
            '/path/baz1': 'baz1',
            '/path/baz2': 'baz2',
            })
