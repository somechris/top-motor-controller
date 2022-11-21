# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from bluepy import btle

from toy_motor_controller.bus.bluez import restart_scanners


class Peripheral(object):
    def __init__(self, address=None):
        self.peripheral = btle.Peripheral(deviceAddr=address)

        # Grabbing a new Peripheral breaks running scanners. So we restart
        # them.
        restart_scanners()

    def disconnect(self):
        return self.peripheral.disconnect()

    def __enter__(self):
        return self

    def __exit__(self):
        self.disconnect()

    def getCharacteristic(self, uuid):
        ret = None
        characteristics = self.peripheral.getCharacteristics(uuid=uuid)
        if characteristics:
            ret = characteristics[0]
        return ret

    def _getServices(self):
        return self.peripheral.getServices()
