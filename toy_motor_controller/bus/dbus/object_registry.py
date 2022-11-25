# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import threading

from toy_motor_controller.util import \
    get_fully_qualified_inherited_class_names

import logging
logger = logging.getLogger(__name__)


class ObjectRegistry():
    def __init__(self, base_path):
        self._base_path = base_path
        self._registry_lock = threading.Lock()
        self._registry = {}
        self._name_mapping = {}

    def map_name(self, name, mapped):
        self._name_mapping[name] = mapped

    def _get_new_index(self, name):
        with self._registry_lock:
            value = self._registry.get(name, 0) + 1
            self._registry[name] = value
        return value

    def _get_mapped_name(self, obj):
        for name in get_fully_qualified_inherited_class_names(obj):
            try:
                mapped = self._name_mapping[name]
                return mapped
            except KeyError:
                # name was not in the name mapping dict, so we need to
                # continue to search with the next name.
                pass
        # None of the name mapping entries matched the inheritance
        # tree of obj. So we use a fallback name
        return 'object'

    def create_path(self, obj):
        name = self._get_mapped_name(obj)
        index = self._get_new_index(name)
        return f'{self._base_path}/{name}{index}'
