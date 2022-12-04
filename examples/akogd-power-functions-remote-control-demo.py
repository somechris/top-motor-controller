#!/usr/bin/python3
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import time

import toy_motor_controller
from toy_motor_controller.toy import AkogdPowerFunctionsRemoteControl

print('Starting toy-motor-controller')
toy_motor_controller.start()

print('Searching for connectable AKOGD Power Functions hubs ...')
device = AkogdPowerFunctionsRemoteControl().connectFirst()

print(f'Device found, connection established: {device}')

print('Full speed on all outputs for 2 seconds')
device.A = 100
device.B = 100
device.C = 100
device.D = 100
time.sleep(2)

print('Stopping all outputs')
device.A = 0
device.B = 0
device.C = 0
device.D = 0
time.sleep(1)

print('Cleaning up')
device.disconnect()
toy_motor_controller.stop()
