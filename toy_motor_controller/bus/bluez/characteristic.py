# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from bluepy import btle


class Characteristic(object):
    def __init__(self, remote_address, uuid):
        self._remote_address = remote_address
        self._uuid = uuid
        self._connect()

    def _connect(self):
        device = btle.Peripheral(self._remote_address)
        handles = device.getCharacteristics(uuid=self._uuid)
        self._handle = handles[0]

    def write(self, value):
        self._handle.write(value)
