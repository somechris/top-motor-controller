# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus.service
import toy_motor_controller.bus.dbus

from toy_motor_controller.bus.dbus import PropertiesObject

from . import get_advertisement_manager
from . import LE_ADVERTISEMENT_IFACE
from . import Registree


class Advertisement(Registree, PropertiesObject):
    def __init__(self):
        super().__init__(
            manager=get_advertisement_manager(),
            main_interface=LE_ADVERTISEMENT_IFACE)

        self._local_name = None
        self._manufacturer_data = None

    def advertise(self):
        self._manager.advertise(self)

    def unadvertise(self):
        self._manager.unadvertise(self)

    def _set_manufacturer_data(self, data):
        self._manufacturer_data = dbus.Dictionary({}, signature='qv')
        if data and len(data) >= 2:
            company_id = (data[1] << 8) + data[0]
            company_data = dbus.Array(data[2:], signature='y')
            self._manufacturer_data[company_id] = company_data

        self._manager.update(self)

    def _set_local_name(self, local_name):
        self._local_name = local_name

        self._manager.update(self)

    def _get_main_interface_properties(self):
        properties = {
            'Type': dbus.String('peripheral'),
            'MinInterval': dbus.UInt32(50),
            'MaxInterval': dbus.UInt32(150),
            }

        if self._local_name is not None:
            properties['LocalName'] = dbus.String(self._local_name)

        if self._manufacturer_data is not None:
            properties['ManufacturerData'] = dbus.Dictionary(
                self._manufacturer_data, signature='qv')

        return properties

    @dbus.service.method(toy_motor_controller.bus.dbus.OM_IFACE,
                         in_signature='',
                         out_signature='a{sv}')
    def GetManagedObjects(self):
        return dbus.Dictionary({}, signature='sv')

    @dbus.service.method(LE_ADVERTISEMENT_IFACE,
                         in_signature='',
                         out_signature='')
    def Release(self):
        pass
