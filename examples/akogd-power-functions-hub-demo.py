#!/usr/bin/python3
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import toy_motor_controller
from toy_motor_controller.toy import AkogdPowerFunctionsHub

print('Starting toy-motor-controller')
toy_motor_controller.start()

print('Searching for connectable AKOGD Power Functions remote controls ...')
device = AkogdPowerFunctionsHub().connectFirst()

print(f'Device found, connection established: {device}')


# When pressing buttons on the remote control, this callback will (after
# registration, see below) produce output like:
#
# New state: {'A': 0, 'B': 0, 'C': 0, 'D': 0}
# New state: {'A': 100, 'B': 0, 'C': 0, 'D': 0}
# New state: {'A': 0, 'B': 0, 'C': 0, 'D': 0}
# New state: {'A': 0, 'B': 0, 'C': -100, 'D': -100}
#
def callback(state, old_state):
    print(f'New state: {state}')


print('Registering callback ...')
device.register_state_change(callback)

print('Callback registered.')
print()
print('Now, press buttons on the remote control...')
input('(Once you are done, press Enter on your keyboard to quit)\n')

print('Cleaning up')
device.unregister_state_change(callback)
device.disconnect()
toy_motor_controller.stop()
