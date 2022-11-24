# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .. import __version__

import dbus

from toy_motor_controller.util import singleton_getter

from .dbus_wrapper import DBus, OM_IFACE, PROPS_IFACE
from .invalid_args_exception import InvalidArgsException

get_dbus = singleton_getter(DBus, lambda: (dbus.SystemBus(),))


__all__ = (
    get_dbus,
    OM_IFACE,
    PROPS_IFACE,
    InvalidArgsException,
    )

__version__ = __version__
