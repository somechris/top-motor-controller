# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus
import dbus.service

import toy_motor_controller.bus.dbus
from toy_motor_controller.bus.bluez import GATT_SERVICE_IFACE


class Service(toy_motor_controller.bus.dbus.PropertiesObject):
    def __init__(self, uuid, primary=False):
        super().__init__(GATT_SERVICE_IFACE)

        self._application = None
        self._uuid = uuid
        self._primary = primary
        self._characteristics = []

    def bind(self, application):
        if self._application == application:
            # We're bound to the application already.
            # Nothing to do.
            return

        if self._application is not None:
            self.unbind()

        self._application = application
        self._application.add(self)

    def unbind(self):
        if self._application is None:
            # We're unbound already, nothing to do
            return

        self._application.remove(self)
        self._application = None

    def add(self, characteristic):
        if characteristic in self._characteristics:
            # Already bound. Nothing to do
            return

        self._characteristics.append(characteristic)
        characteristic.bind(self)

        self.update()

    def remove(self, characteristic):
        if characteristic not in self._characteristics:
            # Not bound. Nothing to do
            return

        self._characteristics.remove(characteristic)
        characteristic.unbind()

        self.update()

    def update(self):
        if self._application is not None:
            self._application.update()

    def enlist_as_managed_property_object(self, mapping):
        super().enlist_as_managed_property_object(mapping)
        for characteristic in self._characteristics:
            characteristic.enlist_as_managed_property_object(mapping)

    def _get_main_interface_properties(self):
        characteristics_paths = [dbus.ObjectPath(characteristic.dbus_path)
                                 for characteristic in self._characteristics]
        return {
            'UUID': self._uuid,
            'Primary': self._primary,
            'Characteristics': dbus.Array(
                characteristics_paths, signature='o'),
            }
