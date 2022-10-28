# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus
import dbus.service

import logging
logger = logging.getLogger(__name__)

OM_IFACE = 'org.freedesktop.DBus.ObjectManager'
PROPS_IFACE = 'org.freedesktop.DBus.Properties'


class DBus(object):
    def __init__(self, bus):
        self._bus = bus

    def init_object(self, obj, path):
        logger.debug(f'Initializing object {obj} at path {path}')
        dbus.service.Object.__init__(obj, self._bus, path)

    def get_object(self, bus, path):
        return self._bus.get_object(bus, path)

    def get_iface(self, obj, iface):
        return dbus.Interface(obj, iface)

    def get_om_iface(self, obj):
        return self.get_iface(obj, OM_IFACE)

    def get_props_iface(self, obj):
        return self.get_iface(obj, PROPS_IFACE)
