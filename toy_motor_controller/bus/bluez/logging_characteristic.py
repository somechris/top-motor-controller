# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import Characteristic

import logging
logger = logging.getLogger(__name__)


class LoggingCharacteristic(Characteristic):
    def read(self, address, offset, link, mtu, type_):
        logger.info(
            f'Read of characteristic={self}, address={address}, '
            f'offset={offset}, link={link}, mtu={mtu}, type={type_}')
        return []

    def write(self, value, address, offset, link, mtu, type_):
        logger.info(
            f'Write of value {value} to characteristic={self}, '
            f'address={address}, offset={offset}, link={link}, mtu={mtu}, '
            f'type={type_}')

    def start_notify(self):
        logger.info('Start notify')

    def stop_notify(self):
        logger.info('Stop notify')
