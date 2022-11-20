#!/usr/bin/python3
# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import argparse
import logging

import toy_motor_controller
from toy_motor_controller.bus.bluez import get_scanner

LOG_FORMAT = ('%(asctime)s.%(msecs)03d %(levelname)-5s [%(threadName)s] '
              '%(filename)s:%(lineno)d - %(message)s')
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(__name__)


def get_dumper(rawData, min_rssi, address):
    if address is not None:
        address = address.lower()

    def dumper(advertisement):
        if min_rssi is None or min_rssi <= advertisement.rssi:
            if address is None or address == advertisement.address.lower():
                print(advertisement.__str__(rawData=rawData))
    return dumper


def main(args):
    logger.debug('Starting toy-motor-controller')
    toy_motor_controller.start()

    logger.debug('Initializing scanner')
    scanner = get_scanner(active=args.active)
    dumper = get_dumper(
        rawData=args.raw_data, min_rssi=args.min_rssi, address=args.address)

    logger.debug('Starting scanner')
    scanner.register(dumper)

    if not args.silent:
        print('Press the enter key to stop the scanner')
    input()

    logger.debug('Cleaning up')
    scanner.unregister(dumper)
    toy_motor_controller.stop()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Bluetooth Advertisement Dumper',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--verbose', '-v',
                        default=0,
                        action='count',
                        help='increase verbosity')

    parser.add_argument('--silent',
                        action='store_true',
                        help='dump only found advertisements')

    parser.add_argument('--raw-data',
                        action='store_true',
                        help='show numeric advertisement keys')

    parser.add_argument('--min-rssi',
                        type=int, default=None,
                        help='Hide advertisements with rssi below this value')

    parser.add_argument('--active',
                        action='store_true',
                        help='perform active (instead of the default passive) '
                        'scans')

    parser.add_argument('--address',
                        default=None,
                        help='only show matches from this address')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.silent:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    main(args)
