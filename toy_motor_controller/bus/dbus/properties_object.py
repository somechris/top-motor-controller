# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus
import dbus.service

from . import Object, InvalidArgsException, PROPS_IFACE


class PropertiesObject(Object):
    def __init__(self, main_interface=None, **kwargs):
        super().__init__(**kwargs)
        self._main_interface = main_interface

    def _get_main_interface_properties(self):
        return {}

    def enlist_as_managed_property_object(self, mapping):
        mapping[self.dbus_path] = {
            self._main_interface: self._get_main_interface_properties()
            }

    @dbus.service.method(PROPS_IFACE, in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != self._main_interface:
            raise InvalidArgsException()

        return self._get_main_interface_properties()
