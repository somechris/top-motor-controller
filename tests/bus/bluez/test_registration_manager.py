# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from unittest.mock import Mock

from toy_motor_controller.bus.bluez import RegistrationManager, \
    RegistrationError

from tests import BasicTestCase


class RegistrationManagerTestCase(BasicTestCase):
    def createRegistrationManager(self, register_actions=[]):
        backend_manager = Mock()
        backend_manager.registration_calls = []

        side_effect_register_counter = 0

        def side_effect_register(path, opt, reply_handler, error_handler):
            nonlocal side_effect_register_counter

            try:
                if side_effect_register_counter < len(register_actions) \
                        and register_actions[side_effect_register_counter]:
                    reply_handler()
                else:
                    error_handler(
                        f'call-{side_effect_register_counter}-failed')
            finally:
                side_effect_register_counter += 1

            backend_manager.registration_calls.append('register')

        def side_effect_unregister(path):
            backend_manager.registration_calls.append('unregister')

        backend_manager.RegisterFacetBar = Mock()
        backend_manager.RegisterFacetBar.side_effect = side_effect_register

        backend_manager.UnregisterFacetBar = Mock()
        backend_manager.UnregisterFacetBar.side_effect = side_effect_unregister

        adapter = Mock()
        adapter.get_interface = Mock(return_value=backend_manager)
        adapter.dbus_init_object = Mock()

        registration_manager = RegistrationManager(
            adapter, 'iface-foo', 'FacetBar')

        adapter.assert_not_called()
        adapter.get_interface.assert_called_once_with('iface-foo')
        adapter.get_interface.reset_mock()
        adapter.dbus_init_object.assert_not_called()

        backend_manager.assert_not_called()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        return (registration_manager, adapter, backend_manager)

    def test_single_unregistered(self):
        (manager, adapter, backend_manager) = self.createRegistrationManager()

        manager.manage('FOO')

        adapter.dbus_init_object.assert_called_once_with(
            'FOO', '/org/bluez/example/facetbar0')

        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

    def test_multiple_unregistered(self):
        (manager, adapter, backend_manager) = self.createRegistrationManager()

        manager.manage('FOO')

        adapter.dbus_init_object.assert_called_once_with(
            'FOO', '/org/bluez/example/facetbar0')
        adapter.dbus_init_object.reset_mock()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.manage('BAR')

        adapter.dbus_init_object.assert_called_once_with(
            'BAR', '/org/bluez/example/facetbar1')
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

    def test_single_plain_registration(self):
        (manager, adapter, backend_manager) = self.createRegistrationManager(
            [True])

        manager.manage('FOO')

        adapter.dbus_init_object.assert_called_once_with(
            'FOO', '/org/bluez/example/facetbar0')
        adapter.dbus_init_object.reset_mock()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.register('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.RegisterFacetBar.assert_called_once()
        self.assertEqual(backend_manager.RegisterFacetBar.call_args.args,
                         ('/org/bluez/example/facetbar0', {}))
        backend_manager.RegisterFacetBar.reset_mock()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.unregister('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_called_once_with(
            '/org/bluez/example/facetbar0')
        backend_manager.UnregisterFacetBar.reset_mock()

    def test_single_double_registration(self):
        (manager, adapter, backend_manager) = self.createRegistrationManager(
            [True])

        manager.manage('FOO')

        adapter.dbus_init_object.assert_called_once_with(
            'FOO', '/org/bluez/example/facetbar0')
        adapter.dbus_init_object.reset_mock()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.register('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.RegisterFacetBar.assert_called_once()
        self.assertEqual(backend_manager.RegisterFacetBar.call_args.args,
                         ('/org/bluez/example/facetbar0', {}))
        backend_manager.RegisterFacetBar.reset_mock()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.register('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.unregister('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_called_once_with(
            '/org/bluez/example/facetbar0')
        backend_manager.UnregisterFacetBar.reset_mock()

        manager.unregister('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

    def test_single_reregistration(self):
        (manager, adapter, backend_manager) = self.createRegistrationManager(
            [True, True])

        manager.manage('FOO')

        adapter.dbus_init_object.assert_called_once_with(
            'FOO', '/org/bluez/example/facetbar0')
        adapter.dbus_init_object.reset_mock()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.register('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.RegisterFacetBar.assert_called_once()
        self.assertEqual(backend_manager.RegisterFacetBar.call_args.args,
                         ('/org/bluez/example/facetbar0', {}))
        backend_manager.RegisterFacetBar.reset_mock()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.unregister('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_called_once_with(
            '/org/bluez/example/facetbar0')
        backend_manager.UnregisterFacetBar.reset_mock()

        manager.register('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.RegisterFacetBar.assert_called_once()
        self.assertEqual(backend_manager.RegisterFacetBar.call_args.args,
                         ('/org/bluez/example/facetbar0', {}))
        backend_manager.RegisterFacetBar.reset_mock()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.unregister('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_called_once_with(
            '/org/bluez/example/facetbar0')
        backend_manager.UnregisterFacetBar.reset_mock()

    def test_single_reregistration_after_failure(self):
        (manager, adapter, backend_manager) = self.createRegistrationManager(
            [False, True])

        manager.manage('FOO')

        adapter.dbus_init_object.assert_called_once_with(
            'FOO', '/org/bluez/example/facetbar0')
        adapter.dbus_init_object.reset_mock()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        with self.assertRaises(RegistrationError):
            manager.register('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.RegisterFacetBar.assert_called_once()
        self.assertEqual(backend_manager.RegisterFacetBar.call_args.args,
                         ('/org/bluez/example/facetbar0', {}))
        backend_manager.RegisterFacetBar.reset_mock()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.register('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.RegisterFacetBar.assert_called_once()
        self.assertEqual(backend_manager.RegisterFacetBar.call_args.args,
                         ('/org/bluez/example/facetbar0', {}))
        backend_manager.RegisterFacetBar.reset_mock()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.unregister('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_called_once_with(
            '/org/bluez/example/facetbar0')
        backend_manager.UnregisterFacetBar.reset_mock()

        manager.unregister('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.reset_mock()

    def test_single_update_unregisterted(self):
        (manager, adapter, backend_manager) = self.createRegistrationManager()

        manager.manage('FOO')

        adapter.dbus_init_object.assert_called_once_with(
            'FOO', '/org/bluez/example/facetbar0')
        adapter.dbus_init_object.reset_mock()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.update('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

    def test_single_update_registerted(self):
        (manager, adapter, backend_manager) = self.createRegistrationManager(
            [True, True])

        manager.manage('FOO')

        adapter.dbus_init_object.assert_called_once_with(
            'FOO', '/org/bluez/example/facetbar0')
        adapter.dbus_init_object.reset_mock()
        backend_manager.RegisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.register('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.RegisterFacetBar.assert_called_once()
        self.assertEqual(backend_manager.RegisterFacetBar.call_args.args,
                         ('/org/bluez/example/facetbar0', {}))
        backend_manager.RegisterFacetBar.reset_mock()
        backend_manager.UnregisterFacetBar.assert_not_called()

        manager.update('FOO')

        adapter.dbus_init_object.assert_not_called()
        self.assertEqual(backend_manager.RegisterFacetBar.call_args.args,
                         ('/org/bluez/example/facetbar0', {}))
        backend_manager.RegisterFacetBar.reset_mock()
        backend_manager.UnregisterFacetBar.assert_called_once_with(
            '/org/bluez/example/facetbar0')
        backend_manager.UnregisterFacetBar.reset_mock()

        manager.unregister('FOO')

        adapter.dbus_init_object.assert_not_called()
        backend_manager.ReregisterFacetBar.assert_not_called()
        backend_manager.UnregisterFacetBar.assert_called_once_with(
            '/org/bluez/example/facetbar0')
        backend_manager.UnregisterFacetBar.reset_mock()

        self.assertEqual(backend_manager.registration_calls,
                         ['register', 'unregister', 'register', 'unregister'])
