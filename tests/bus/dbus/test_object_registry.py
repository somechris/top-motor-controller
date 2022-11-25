# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from toy_motor_controller.bus.dbus import ObjectRegistry

from tests import BasicTestCase


class ObjectRegistryTestCase(BasicTestCase):
    def create_registry(self):
        return ObjectRegistry('base-foo')

    def test_create_path_plain_object(self):
        registry = self.create_registry()

        actual = registry.create_path(object())

        self.assertEqual(actual, 'base-foo/object1')

    def test_create_path_plain_multiple_objects(self):
        registry = self.create_registry()

        actual = registry.create_path(object())

        self.assertEqual(actual, 'base-foo/object1')

        actual = registry.create_path(object())

        self.assertEqual(actual, 'base-foo/object2')

    def test_create_path_unregistered_class(self):
        registry = self.create_registry()

        actual = registry.create_path(self.clsA())

        self.assertEqual(actual, 'base-foo/object1')

    def test_create_path_registered_class(self):
        registry = self.create_registry()
        registry.map_name(
            'tests.bus.dbus.test_object_registry.ObjectRegistryTestCase.clsA',
            'BAR')

        actual = registry.create_path(self.clsA())

        self.assertEqual(actual, 'base-foo/BAR1')

    def test_create_path_registered_subclass(self):
        registry = self.create_registry()
        registry.map_name(
            'tests.bus.dbus.test_object_registry.ObjectRegistryTestCase.clsB',
            'BAR')

        actual = registry.create_path(self.clsAB())

        self.assertEqual(actual, 'base-foo/BAR1')

    def test_create_path_registered_mix(self):
        registry = self.create_registry()
        registry.map_name(
            'tests.bus.dbus.test_object_registry.ObjectRegistryTestCase.clsB',
            'BAR')

        actual = registry.create_path(self.clsB())

        self.assertEqual(actual, 'base-foo/BAR1')

        actual = registry.create_path(self.clsAB())

        self.assertEqual(actual, 'base-foo/BAR2')

        actual = registry.create_path(self.clsB())

        self.assertEqual(actual, 'base-foo/BAR3')

        actual = registry.create_path(self.clsA())

        self.assertEqual(actual, 'base-foo/object1')

        actual = registry.create_path('3')

        self.assertEqual(actual, 'base-foo/object2')

        actual = registry.create_path(self.clsAB())

        self.assertEqual(actual, 'base-foo/BAR4')

    class clsA():
        pass

    class clsB():
        pass

    class clsAB(clsA, clsB):
        pass
