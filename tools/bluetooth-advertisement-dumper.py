#!/usr/bin/python3
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import toy_motor_controller
from toy_motor_controller.bus.bluez import get_scanner

print('Starting toy-motor-controller')
toy_motor_controller.start()

print('Initializing scanner')
scanner = get_scanner()


def dumper(advertisement):
    print(advertisement)


print('Starting scanner')
scanner.register(dumper)

input('\nPress the enter key to stop the scanner again\n\n')

print('Cleaning up')
scanner.unregister(dumper)
toy_motor_controller.stop()
