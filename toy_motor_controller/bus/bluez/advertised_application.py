# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from . import Advertisement, Application


class AdvertisedApplication(Advertisement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._application = Application()

    def advertise(self):
        self.register(self)

    def unadvertise(self):
        self.unregister(self)

    def register(self):
        self._application.register()
        super().register()

    def unregister(self):
        super().unregister()
        self._application.unregister()

    def add(self, service):
        self._application.add(service)

    def remove(self, service):
        self._application.remove(service)
