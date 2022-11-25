# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus

from unittest.mock import patch, Mock

from toy_motor_controller.bus.dbus import InvalidArgsException
from toy_motor_controller.bus.bluez import Descriptor
from toy_motor_controller.bus.bluez import GATT_DESCRIPTOR_IFACE

from tests import BasicTestCase


class DescriptorTestCase(BasicTestCase):
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_unbound(self, init):
        characteristic = Mock()
        characteristic.add = Mock()

        descriptor = Descriptor('uuid-foo')
        descriptor.bind(characteristic)

        characteristic.add.assert_called_once_with(descriptor)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_bound_same(self, init):
        characteristic = Mock()
        characteristic.add = Mock()

        descriptor = Descriptor('uuid-foo')
        descriptor.bind(characteristic)
        descriptor.bind(characteristic)

        characteristic.add.assert_called_once_with(descriptor)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_bind_bound_different(self, init):
        characteristicA = Mock()
        characteristicA.add = Mock()
        characteristicA.remove = Mock()

        characteristicB = Mock()
        characteristicB.add = Mock()

        descriptor = Descriptor('uuid-foo')
        descriptor.bind(characteristicA)
        descriptor.bind(characteristicB)

        characteristicA.add.assert_called_once_with(descriptor)
        characteristicA.remove.assert_called_once_with(descriptor)

        characteristicB.add.assert_called_once_with(descriptor)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_unbind_unbound(self, init):
        descriptor = Descriptor('uuid-foo')

        descriptor.unbind()

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_unbind_bound(self, init):
        characteristic = Mock()
        characteristic.add = Mock()
        characteristic.remove = Mock()

        descriptor = Descriptor('uuid-foo')
        descriptor.bind(characteristic)
        descriptor.unbind()

        characteristic.add.assert_called_once_with(descriptor)
        characteristic.remove.assert_called_once_with(descriptor)

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_default_unbound(self, init):
        descriptor = Descriptor('uuid-foo')

        actual = descriptor.GetAll(GATT_DESCRIPTOR_IFACE)

        self.assertEqual(actual, {
                'Characteristic': None,
                'UUID': 'uuid-foo',
                'Flags': [],
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_default_bound(self, init):
        characteristic = Mock()
        characteristic.dbus_path = '/path/bar'

        descriptor = Descriptor('uuid-foo')
        descriptor.bind(characteristic)

        actual = descriptor.GetAll(GATT_DESCRIPTOR_IFACE)

        self.assertEqual(actual, {
                'Characteristic': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': [],
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_read(self, init):
        characteristic = Mock()
        characteristic.dbus_path = '/path/bar'

        descriptor = Descriptor('uuid-foo', read=True)
        descriptor.bind(characteristic)

        actual = descriptor.GetAll(GATT_DESCRIPTOR_IFACE)

        self.assertEqual(actual, {
                'Characteristic': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['read'],
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_write(self, init):
        characteristic = Mock()
        characteristic.dbus_path = '/path/bar'

        descriptor = Descriptor('uuid-foo', write=True)
        descriptor.bind(characteristic)

        actual = descriptor.GetAll(GATT_DESCRIPTOR_IFACE)

        self.assertEqual(actual, {
                'Characteristic': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['write'],
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_all(self, init):
        characteristic = Mock()
        characteristic.dbus_path = '/path/bar'

        descriptor = Descriptor('uuid-foo', read=True, write=True)
        descriptor.bind(characteristic)

        actual = descriptor.GetAll(GATT_DESCRIPTOR_IFACE)

        self.assertEqual(actual, {
                'Characteristic': dbus.ObjectPath('/path/bar'),
                'UUID': 'uuid-foo',
                'Flags': ['read', 'write'],
                })

    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_properties_wrong_interface(self, init):
        characteristic = Mock()
        characteristic.dbus_path = '/path/bar'

        descriptor = Descriptor('uuid-foo', read=True)

        with self.assertRaises(InvalidArgsException):
            descriptor.GetAll('foo')
