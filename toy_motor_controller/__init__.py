# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import threading

import dbus.mainloop.glib
from gi.repository import GLib

MAINLOOP = None


def start():
    global MAINLOOP

    if MAINLOOP is None:
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        MAINLOOP = GLib.MainLoop()

        threading.Thread(target=MAINLOOP.run, args=(), daemon=True).start()

    return MAINLOOP


def stop():
    if MAINLOOP is not None:
        MAINLOOP.quit()


__version__ = '0.0.1-alpha.0'
