#!/usr/bin/python3
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import time

import toy_motor_controller
from toy_motor_controller.toy import PlaymobilRcRacersRemoteControl

print('Starting toy-motor-controller')
toy_motor_controller.start()

print('Searching for connectable Playmobil RC Racers vehicles ...')
device = PlaymobilRcRacersRemoteControl().connectFirst()

print(f'Device found, connection established: {device}')

print('Turn light on/off ...')
device.light = True
time.sleep(1)
device.light = False
time.sleep(1)

print('Wiggle wheels ..')
device.direction = -100
time.sleep(1)
device.direction = 100
time.sleep(1)
device.direction = 0

# # Uncomment the following lines to slowly (speed_multiplier line) move
# # forward (speed line).
# device.speed_multiplier = -100
# device.speed = 100
# time.sleep(2)

print('Stopping ...')
device.speed = 0

print('Cleaning up')
device.disconnect()
toy_motor_controller.stop()
