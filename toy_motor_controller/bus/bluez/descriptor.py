# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus
import dbus.service

from toy_motor_controller.bus.dbus import PropertiesObject
from toy_motor_controller.bus.bluez import GATT_DESCRIPTOR_IFACE
from toy_motor_controller.bus.bluez import normalize_io_options


class Descriptor(PropertiesObject):
    def __init__(
            self, uuid, read=False, write=False):
        super().__init__(GATT_DESCRIPTOR_IFACE)

        self._characteristic = None
        self._uuid = uuid

        self._flags = [key for key, value in {
                'read': read,
                'write': write,
                }.items() if value]

    def bind(self, characteristic):
        if self._characteristic == characteristic:
            # We're bound to the characteristic already.
            # Nothing to do.
            return

        if self._characteristic is not None:
            self.unbind()

        self._characteristic = characteristic
        self._characteristic.add(self)

    def unbind(self):
        if self._characteristic is None:
            # We're unbound already, nothing to do
            return

        self._characteristic.remove(self)
        self._characteristic = None

    def _get_main_interface_properties(self):
        characteristic_path = None
        if self._characteristic:
            characteristic_path = dbus.ObjectPath(
                self._characteristic.dbus_path)
        return {
            'Characteristic': characteristic_path,
            'UUID': self._uuid,
            'Flags': self._flags,
            }

    @dbus.service.method(GATT_DESCRIPTOR_IFACE,
                         in_signature='a{sv}',
                         out_signature='ay')
    def ReadValue(self, options):
        value = self.read(**normalize_io_options(options))
        return dbus.Array(value, signature='y')

    @dbus.service.method(GATT_DESCRIPTOR_IFACE, in_signature='aya{sv}')
    def WriteValue(self, value, options):
        byte_value = [int(byte) for byte in value]
        self.write(byte_value, **normalize_io_options(options))

    def read(self, address, offset, link, mtu, type_):
        return []

    def write(self, value, address, offset, link, mtu, type_):
        pass
