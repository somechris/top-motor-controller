# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

class Characteristic(object):
    def __init__(self, backend_characteristic):
        self._backend_characteristic = backend_characteristic

    def write(self, value):
        self._backend_characteristic.write(value)
