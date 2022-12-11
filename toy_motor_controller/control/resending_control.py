# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import time

from toy_motor_controller.util import NamedThread


def resending_control(interval=1):
    def initializer(setter):
        _setter = setter
        _instance = None
        _value = None

        def resender():
            while True:
                if _instance is not None:
                    _setter(_instance, _value)
                time.sleep(interval)

        NamedThread(name="resender", target=resender, args=(),
                    daemon=True).start()

        def setter_and_updater(instance, value):
            nonlocal _instance
            nonlocal _value
            _value = value
            _instance = instance
            setter(instance, value)

        return setter_and_updater
    return initializer
