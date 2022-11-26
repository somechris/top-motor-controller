# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import toy_motor_controller.bus.dbus


class Registree(toy_motor_controller.bus.dbus.Object):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)

        self._manager = manager
        self._manager.manage(self)

    def register(self):
        self._manager.register(self)

    def unregister(self):
        self._manager.unregister(self)

    @property
    def address(self):
        return self._manager.address

    @property
    def address_type(self):
        return self._manager.address_type

    @property
    def name(self):
        return self._manager.name

    @property
    def alias(self):
        return self._manager.alias
