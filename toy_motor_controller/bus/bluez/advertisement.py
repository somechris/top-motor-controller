# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus.service
import toy_motor_controller.bus.dbus

from . import get_advertisement_manager
from . import LE_ADVERTISEMENT_IFACE


class Advertisement(dbus.service.Object):
    def __init__(self):
        super(Advertisement, self).__init__()

        self._manufacturer_data = None

        self._manager = get_advertisement_manager()
        self._manager.republish(self)

    def _set_manufacturer_data(self, data):
        self._manufacturer_data = dbus.Dictionary({}, signature='qv')
        self._manufacturer_data[0xffff] = dbus.Array(data, signature='y')

        self._manager.republish(self)

    @dbus.service.method(toy_motor_controller.bus.dbus.PROPS_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != LE_ADVERTISEMENT_IFACE:
            raise toy_motor_controller.bus.dbus.InvalidArgsException()

        properties = {
            'Type': dbus.String('peripheral'),
            'MinInterval': dbus.UInt32(50),
            'MaxInterval': dbus.UInt32(150),
            }

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
