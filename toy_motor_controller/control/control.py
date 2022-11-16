# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

class Control(object):
    def __init__(self, setter, initial_value=None):
        self._reported_value = self._convert_to_reported_value(initial_value)
        self._backend_setter = setter

    def get(self, instance):
        return self._reported_value

    def set(self, instance, value):
        self._reported_value = self._convert_to_reported_value(value)

        backend_value = self._convert_reported_to_backend_value(
            self._reported_value)

        self._backend_setter(instance, backend_value)

    def _convert_to_reported_value(self, value):
        return value

    def _convert_reported_to_backend_value(self, value):
        return value
