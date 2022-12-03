# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import pprint

import dbus

import toy_motor_controller.bus.dbus
from . import get_application_manager
from . import Registree

import logging
logger = logging.getLogger(__name__)


class Application(Registree):
    def __init__(self, **kwargs):
        super().__init__(manager=get_application_manager(), **kwargs)
        self._services = []

    def add(self, service):
        if service in self._services:
            # Already bound. Nothing to do
            return

        self._services.append(service)
        service.bind(self)

        self.update()

    def remove(self, service):
        if service not in self._services:
            # Not bound. Nothing to do
            return

        self._services.remove(service)
        service.unbind()

        self.update()

    @dbus.service.method(toy_motor_controller.bus.dbus.OM_IFACE,
                         out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        ret = {}

        for service in self._services:
            service.enlist_as_managed_property_object(ret)

        logger.debug(f'ManagedObjects of Application:\n{pprint.pformat(ret)}')

        return ret
