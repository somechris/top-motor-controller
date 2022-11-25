# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus
import dbus.service

import toy_motor_controller.bus.dbus
from toy_motor_controller.bus.dbus import PropertiesObject
from toy_motor_controller.bus.bluez import GATT_CHARACTERISTIC_IFACE
from toy_motor_controller.bus.bluez import normalize_io_options


class Characteristic(PropertiesObject):
    def __init__(
            self, uuid, indicate=False, read=False,
            notify=False, write=False, write_without_response=False):
        super().__init__(GATT_CHARACTERISTIC_IFACE)

        self._service = None
        self._uuid = uuid
        self._descriptors = []

        self._flags = [key for key, value in {
                'indicate': indicate,
                'read': read,
                'notify': notify,
                'write': write,
                'write-without-response': write_without_response,
                }.items() if value]

    def bind(self, service):
        if self._service == service:
            # We're bound to the service already.
            # Nothing to do.
            return

        if self._service is not None:
            self.unbind()

        self._service = service
        self._service.add(self)

    def unbind(self):
        if self._service is None:
            # We're unbound already, nothing to do
            return

        self._service.remove(self)
        self._service = None

    def add(self, descriptor):
        if descriptor in self._descriptors:
            # Already bound. Nothing to do
            return

        self._descriptors.append(descriptor)
        descriptor.bind(self)

        self.update()

    def remove(self, descriptor):
        if descriptor not in self._descriptors:
            # Not bound. Nothing to do
            return

        self._descriptors.remove(descriptor)
        descriptor.unbind()

        self.update()

    def update(self):
        if self._service is not None:
            self._service.update()

    def enlist_as_managed_property_object(self, mapping):
        super().enlist_as_managed_property_object(mapping)
        for descriptor in self._descriptors:
            descriptor.enlist_as_managed_property_object(mapping)

    def _get_main_interface_properties(self):
        service_path = None
        if self._service is not None:
            service_path = dbus.ObjectPath(self._service.dbus_path)

        descriptor_paths = [dbus.ObjectPath(descriptor.dbus_path)
                            for descriptor in self._descriptors]

        return {
            'Service': service_path,
            'UUID': self._uuid,
            'Flags': self._flags,
            'Descriptors': dbus.Array(descriptor_paths, signature='o')
            }

    @dbus.service.method(GATT_CHARACTERISTIC_IFACE,
                         in_signature='a{sv}',
                         out_signature='ay')
    def ReadValue(self, options):
        value = self.read(**normalize_io_options(options))
        return dbus.Array(value, signature='y')

    @dbus.service.method(GATT_CHARACTERISTIC_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        byte_value = [int(byte) for byte in value]
        self.write(byte_value, **normalize_io_options(options))

    @dbus.service.method(GATT_CHARACTERISTIC_IFACE)
    def StartNotify(self):
        self._is_notifying = True
        self.start_notify()

    @dbus.service.method(GATT_CHARACTERISTIC_IFACE)
    def StopNotify(self):
        self.stop_notify()
        self._is_notifying = False

    @dbus.service.signal(toy_motor_controller.bus.dbus.PROPS_IFACE,
                         signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed, invalidated):
        pass

    def read(self, address, offset, link, mtu, type_):
        return []

    def write(self, value, address, offset, link, mtu, type_):
        pass

    def start_notify(self):
        pass

    def stop_notify(self):
        pass

    def update_value(self, value=None, invalidate=False):
        if not self._is_notifying:
            return

        changed = {}
        if value is not None:
            changed['Value'] = value

        invalidated = []
        if invalidate:
            invalidated += ['Value']

        self.PropertiesChanged(
                GATT_CHARACTERISTIC_IFACE,
                dbus.Dictionary(changed, signature='sv'),
                dbus.Array(invalidated, signature='s'))
