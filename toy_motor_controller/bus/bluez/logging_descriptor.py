# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import Descriptor

import logging
logger = logging.getLogger(__name__)


class LoggingDescriptor(Descriptor):
    def read(self, address, offset, link, mtu, type_, device_path):
        logger.info(
            f'Read of descriptor={self}, address={address}, '
            f'offset={offset}, link={link}, mtu={mtu}, type={type_}, '
            f'device_path={device_path}')
        return []

    def write(self, value, address, offset, link, mtu, type_, device_path):
        logger.info(
            f'Write of value {value} to descriptor={self}, '
            f'address={address}, offset={offset}, link={link}, mtu={mtu}, '
            f'type={type_}, device_path={device_path}')
