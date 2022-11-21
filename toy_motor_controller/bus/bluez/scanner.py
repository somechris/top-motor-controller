# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import threading
import time

from bluepy import btle

from . import ScannedAdvertisement

import logging
logger = logging.getLogger(__name__)


class Scanner(object):
    def __init__(self, active=False):
        self._passive = not active

        self._backend = btle.Scanner()
        self._backend.withDelegate(self.Delegate(self))
        self._backend_lock = threading.Lock()
        self._backend_running = False
        self._backend_needs_restart = False
        self._callbacks = []

        threading.Thread(target=self._scan, args=(), daemon=True).start()

    def _start_backend(self):
        with self._backend_lock:
            if not self._backend_running:
                logger.debug('Starting scanner')
                self._backend.start(passive=self._passive)
                self._backend_running = True

    def _stop_backend(self):
        with self._backend_lock:
            if self._backend_running:
                logger.debug('Stopping scanner')
                try:
                    self._backend.stop()
                except btle.BTLEDisconnectError:
                    # The device has already disconnected.
                    # Since we're stopping anyways, we can ignore that.
                    pass
            self._backend_running = False
            self._backend_needs_restart = False

    def restart(self):
        with self._backend_lock:
            self._backend_needs_restart = True

    def _scan(self):
        has_callbacks = False
        had_callbacks = False
        while True:
            if self._backend_needs_restart:
                self._stop_backend()

            if has_callbacks:
                self._start_backend()

                self._backend.process(timeout=3)
            else:
                if had_callbacks:
                    self._stop_backend()
                else:
                    time.sleep(1)

            had_callbacks = has_callbacks
            has_callbacks = len(self._callbacks)

    def register(self, callback):
        self._callbacks.append(callback)

    def unregister(self, callback):
        self._callbacks.remove(callback)

    def _receiveAdvertisement(self, advertisement):
        for callback in self._callbacks:
            callback(advertisement)

    class Delegate(btle.DefaultDelegate):
        def __init__(self, scanner):
            super().__init__()
            self._scanner = scanner

        def handleDiscovery(self, scanEntry, isNewDev, isNewData):
            advertisement = ScannedAdvertisement(scanEntry)
            self._scanner._receiveAdvertisement(advertisement)
