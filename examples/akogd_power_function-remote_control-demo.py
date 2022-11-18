#!/usr/bin/python3
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import time

import toy_motor_controller
from toy_motor_controller.toy import AkogdPowerFunctionRemoteControl

print('Starting toy-motor-controller')
toy_motor_controller.start()

print('Connecting to first found device')
device = AkogdPowerFunctionRemoteControl().connectFirst()

print(f'Connected to {device}')

print('Full speed on all outputs for 2 seconds')
device.a = 100
device.b = 100
device.c = 100
device.d = 100
time.sleep(2)

print('Stopping all outputs')
device.a = 0
device.b = 0
device.c = 0
device.d = 0
time.sleep(1)

print('Disconnecting device')
device.disconnect()

print('Stopping toy-motor-controller')
toy_motor_controller.stop()
