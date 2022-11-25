# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import patch, Mock

from toy_motor_controller.bus.bluez import Application

from tests import BasicTestCase


class ApplicationTestCase(BasicTestCase):
    @patch('toy_motor_controller.bus.bluez.Application.dbus_path', '/path/foo')
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_single(self, init):
        service = Mock()
        service.bind = Mock()
        service.unbind = Mock()

        application = Application()
        application._object_path = '/path/foo'
        application.add(service)

        service.bind.assert_called_once_with(application)
        service.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.bluez.Application.dbus_path', '/path/foo')
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_multiple(self, init):
        service1 = Mock()
        service1.bind = Mock()
        service1.unbind = Mock()

        service2 = Mock()
        service2.bind = Mock()
        service2.unbind = Mock()

        application = Application()
        application._object_path = '/path/foo'
        application.add(service1)
        application.add(service2)

        service1.bind.assert_called_once_with(application)
        service1.unbind.assert_not_called()

        service2.bind.assert_called_once_with(application)
        service2.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.bluez.Application.dbus_path', '/path/foo')
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_add_same_twice(self, init):
        service = Mock()
        service.bind = Mock()
        service.unbind = Mock()

        application = Application()
        application._object_path = '/path/foo'
        application.add(service)
        application.add(service)

        service.bind.assert_called_once_with(application)
        service.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.bluez.Application.dbus_path', '/path/foo')
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_remove_not_added(self, init):
        service = Mock()
        service.bind = Mock()
        service.unbind = Mock()

        application = Application()
        application._object_path = '/path/foo'
        application.remove(service)

        service.bind.assert_not_called()
        service.unbind.assert_not_called()

    @patch('toy_motor_controller.bus.bluez.Application.dbus_path', '/path/foo')
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_remove_plain(self, init):
        service = Mock()
        service.bind = Mock()
        service.unbind = Mock()

        application = Application()
        application._object_path = '/path/foo'
        application.add(service)
        application.remove(service)

        service.bind.assert_called_once_with(application)
        service.unbind.assert_called_once_with()

    @patch('toy_motor_controller.bus.bluez.Application.dbus_path', '/path/foo')
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_GetManagedObjects_no_services(self, init):
        application = Application()

        actual = application.GetManagedObjects()

        self.assertEqual(actual, {})

    @patch('toy_motor_controller.bus.bluez.Application.dbus_path', '/path/foo')
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_GetManagedObjects_single_service(self, init):
        application = Application()
        application._object_path = '/path/foo'

        def service1enlister(obj):
            obj['/path/baz1'] = 'baz1'
        service1 = Mock()
        service1.dbus_path = '/path/baz1'
        service1.enlist_as_managed_property_object = service1enlister
        application.add(service1)

        actual = application.GetManagedObjects()

        self.assertEqual(actual, {'/path/baz1': 'baz1'})

    @patch('toy_motor_controller.bus.bluez.Application.dbus_path', '/path/foo')
    @patch('toy_motor_controller.bus.dbus.Object.__init__')
    def test_GetManagedObjects_multiple_services(self, init):
        application = Application()
        application._object_path = '/path/foo'

        def service1enlister(obj):
            obj['/path/baz1'] = 'baz1'
        service1 = Mock()
        service1.dbus_path = '/path/baz1'
        service1.enlist_as_managed_property_object = service1enlister
        application.add(service1)

        def service2enlister(obj):
            obj['/path/baz2'] = 'baz2'
        service2 = Mock()
        service2.dbus_path = '/path/baz2'
        service2.enlist_as_managed_property_object = service2enlister
        application.add(service2)

        actual = application.GetManagedObjects()

        self.assertEqual(actual, {
                '/path/baz1': 'baz1',
                '/path/baz2': 'baz2',
                })

    class ServiceStub():
        def __init__(self, managed):
            self._managed = managed

        def enlist_as_managed_property_object(self, mapping):
            for key, value in self._managed.items():
                mapping[key] = value
