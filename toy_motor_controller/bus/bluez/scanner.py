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
    def __init__(self):
        self._scanner = btle.Scanner()
        self._scanner.withDelegate(self.Delegate(self))
        self._callbacks = []

        threading.Thread(target=self._scan, args=(), daemon=True).start()

    def _scan(self):
        has_callbacks = False
        had_callbacks = False
        while True:
            if has_callbacks:
                if not had_callbacks:
                    logger.debug('Starting scanner')
                    self._scanner.start(passive=True)

                self._scanner.process(timeout=3)
            else:
                if had_callbacks:
                    logger.debug('Stopping scanner')
                    try:
                        self._scanner.stop()
                    except btle.BTLEDisconnectError:
                        # The device has already disconnected.
                        # Since we're stopping anyways, we can ignore that.
                        pass
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
