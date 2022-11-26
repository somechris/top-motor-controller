# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus
import dbus.service

import toy_motor_controller.bus.dbus

import logging
logger = logging.getLogger(__name__)


class Object(dbus.service.Object):
    def __init__(self, **kwargs):
        bus = toy_motor_controller.bus.dbus.get_dbus()
        object_registry = toy_motor_controller.bus.dbus.\
            get_dbus_object_registry()
        path = object_registry.create_path(self)
        logger.debug(f'Registering {self.__class__.__name__} at {path}')
        super().__init__(bus._get_raw_dbus(), path, **kwargs)

    @property
    def dbus_path(self):
        return self._object_path
