# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import random

import logging
logger = logging.getLogger(__name__)


def randombyte():
    return random.randrange(0, 256)


def bytes_to_hex_string(bytes=[], connector=''):
    return connector.join([f'{byte:02x}' for byte in bytes])


def hex_string_to_bytes(hex_string):
    ret = []
    if len(hex_string) % 2 == 1:
        hex_string = '0' + hex_string
    for offset in range(0, len(hex_string), 2):
        ret.append(int(hex_string[offset:offset+2], 16))
    return ret


def clamped(value, minimum, maximum):
    return min(max(value, minimum), maximum)


def clamped_int(value, minimum, maximum):
    return clamped(int(value+0.5), minimum, maximum)


def singleton_getter(class_, args=lambda: (), key=None, registry=None):
    instance = None

    def get():
        nonlocal instance
        if instance is None:
            extra = ''
            if key is not None:
                extra = f' ({key})'
            logger.debug(f'Creating singleton {class_.__name__}{extra}')
            instance = class_(*args())

            if registry is not None and key is not None:
                registry[key] = instance
        return instance
    return get
