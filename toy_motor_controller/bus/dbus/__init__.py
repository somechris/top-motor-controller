# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import logging
logger = logging.getLogger(__name__)

import dbus

from .dbus_wrapper import DBus, OM_IFACE, PROPS_IFACE
from .invalid_args_exception import InvalidArgsException

DBUS = None


def get_dbus():
    global DBUS
    if DBUS is None:
        logger.debug('Creating singleton dbus')
        DBUS = DBus(dbus.SystemBus())
    return DBUS


__all__ = (
    get_dbus,
    OM_IFACE,
    PROPS_IFACE,
    InvalidArgsException,
    )
