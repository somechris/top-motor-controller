# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import random


def randombyte():
    return random.randrange(0, 256)


def clamped(value, minimum, maximum):
    return min(max(value, minimum), maximum)


def clamped_int(value, minimum, maximum):
    return clamped(int(value+0.5), minimum, maximum)
