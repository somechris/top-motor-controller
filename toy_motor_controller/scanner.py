#!/usr/bin/env python3
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import logging
logger = logging.getLogger(__name__)


from . import start, stop, toy


CLASSES = [
    toy.AkogdPowerFunctionRemoteControl,
]


def print_dict(d):
    keys = (list(d.keys()))
    keys.sort()
    for key in keys:
        if key != 'supplement':
            print(f'  {key}: {d[key]}')


def scan_class(_class):
    instance = _class()
    duration = 5

    print(f'Scanning for {_class.__name__} devices ...')

    for match in instance.scan(duration=duration):
        print()
        print()
        print(f'Found {_class.__name__} device:')

        print_dict(match)
        if 'supplement' in match:
            print_dict(match['supplement'])
            del match['supplement']

        arg_list = []
        keys = (list(match.keys()))
        keys.sort()
        for key in keys:
            arg_list.append(f'{key}={str([match[key]])[1:-1]}')
        args = ', '.join(arg_list)

        main_module = _class.__module__.split(".")[0]
        import_module = '.'.join(_class.__module__.split(".")[0:2])
        demo_name = ('-'.join(_class.__module__.split(".")[-2:]))
        print()
        print('You can connect to the device via:')
        print()
        print('#-----------------------------')
        print(f'import {main_module}')
        print(f'from {import_module} import {_class.__name__}')
        print()
        print(f'{main_module}.start()')
        print(f'device = {_class.__name__}().connect({args})')
        print()
        print('# <Insert your code here>')
        print(f'# See examples/{demo_name}-demo.py')
        print('# for a short demo code')
        print()
        print(f'{main_module}.stop()')
        print('#-----------------------------')


def main():
    start()

    for _class in CLASSES:
        scan_class(_class)

    stop()


if __name__ == '__main__':
    main()
