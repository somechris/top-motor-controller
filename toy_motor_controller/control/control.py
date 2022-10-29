# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

class Control(object):
    def __init__(self, setter, initial_value=None):
        self._value = initial_value
        self._backend_setter = setter

    def get(self, instance):
        return self._value

    def set(self, instance, value):
        self._value = self._coerce_value(value)
        self._backend_setter(instance, self._value)

    def _coerce_value(self, value):
        return value
