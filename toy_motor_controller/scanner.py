#!/usr/bin/env python3
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import argparse

import logging
logger = logging.getLogger(__name__)


from . import start, stop, toy


CLASSES = [
    toy.AkogdPowerFunctionHub,
    toy.AkogdPowerFunctionRemoteControl,
    toy.PlaymobilRacerRemoteControl,
    toy.PlaymobilRacerVehicle,
]


def parse_arguments():
    supported_classes = ',\n '.join([class_.__name__ for class_ in CLASSES])
    parser = argparse.ArgumentParser(
        description='Scans for devices supported by toy-motor-controller. ',
        epilog=f'The following classes are supported: {supported_classes}',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--class',
        default=None,
        help='scan only for this class instead of all supported classes. '
        '(See below for supported classes)')

    parser.add_argument(
        '--duration',
        type=float,
        default=5,
        help='scan duration (in seconds) for each class')

    return parser.parse_args()


def print_dict(d):
    keys = (list(d.keys()))
    keys.sort()
    for key in keys:
        if key != 'supplement':
            print(f'  {key}: {d[key]}')


def scan_class(_class, args):
    instance = _class()
    duration = args.duration

    print(f'Letting {_class.__name__} scan for devices to connect to ...')

    for match in instance.scan(duration=duration, strip_supplement=False):
        print()
        print()
        print(f'{_class.__name__} found a device to connect to:')

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
        print('Here is a code snippet to connect to the device:')
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
        print()
        print()


def main(args):
    class_name = vars(args)['class']
    if class_name is None:
        classes = CLASSES
    else:
        classes = [candidate for candidate in CLASSES
                   if candidate.__name__ == class_name
                   ]

    start()

    for _class in classes:
        scan_class(_class, args)

    stop()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
