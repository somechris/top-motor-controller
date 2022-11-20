# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from bluepy import btle


class Characteristic(object):
    def __init__(self, remote_address, uuid):
        self._remote_address = remote_address
        self._uuid = uuid
        self.connect()

    def connect(self):
        self._device = btle.Peripheral(self._remote_address)
        handles = self._device.getCharacteristics(uuid=self._uuid)
        self._handle = handles[0]

    def disconnect(self):
        if self._device:
            self._device.disconnect()
        self._device = None
        self._handle = None

    def write(self, value):
        self._handle.write(value)
