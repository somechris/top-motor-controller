# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import threading

from . import RegistrationError, REGISTRATION_MANAGER_BASE_PATH

import logging
logger = logging.getLogger(__name__)


class RegistrationManager():
    def __init__(self, adapter, interface, facet):
        self._adapter = adapter
        self._interface = interface
        self._facet = facet

        logger.debug(f'Bringing up {self._interface} ...')

        self._manager = self._adapter.get_interface(interface)

        self._backend_register = self._manager.__getattr__(
            f'Register{self._facet}')
        self._backend_unregister = self._manager.__getattr__(
            f'Unregister{self._facet}')

        self._managed_object_properties = {}

        logger.debug(f'{self._interface} is up and running')

    def manage(self, obj):
        if obj not in self._managed_object_properties:
            try:
                logger.debug(f'Starting to manage {obj}')
            except AttributeError:
                # When shimming objects, _object_path was maybe not yet set
                # up, so dbus.services.Object.__str__ cannot access
                # _object_path and bails out with an attribute error. As this
                # is not fatal for our cause, we at least log the class name.
                logger.debug('Starting to manage on object of '
                             f'{obj.__class__.__name__}')
            properties = {
                'path': path,
                'lock': threading.Lock(),
                'registered': False,
                }
            self._managed_object_properties[obj] = properties

    def unregister(self, obj):
        properties = self._managed_object_properties[obj]
        if properties['registered']:
            with properties['lock']:
                if properties['registered']:
                    self._unregister(properties)

    def _unregister(self, properties):
        path = properties['path']
        logger.debug(f'Unregistering {path}')
        self._backend_unregister(path)
        properties['registered'] = False

    def register(self, obj):
        properties = self._managed_object_properties[obj]
        if not properties['registered']:
            with properties['lock']:
                if not properties['registered']:
                    self._register(properties)

    def _register(self, properties):
        path = properties['path']

        succeeded = None
        error = None

        barrier = threading.Lock()

        def registration_worked():
            nonlocal succeeded
            succeeded = True
            barrier.release()

        def registration_failed(_error):
            nonlocal succeeded
            nonlocal error
            succeeded = False
            error = _error
            barrier.release()

        # At least for Advertisement registration, the synchronous method call
        # will fail, while the asynchronous wethod call succeeds. So we use
        # the asynchronous call and synchronize through a barrier afterwards
        # to the synchronous behaviour.

        barrier.acquire()  # Gets released in registration_{worked,failed}

        self._backend_register(
            path, {},
            reply_handler=registration_worked,
            error_handler=registration_failed)

        barrier.acquire()  # Wait until the callbacks are done.
        barrier.release()  # Releasing again to avoid leaving the lock hanging

        if not succeeded:
            raise RegistrationError(path, error)

        properties['registered'] = True
        logger.debug(f'Registering {path} done')

    def update(self, obj):
        logger.debug(f'Updating {obj}')

        properties = self._managed_object_properties[obj]
        if properties['registered']:
            with properties['lock']:
                if properties['registered']:
                    self._unregister(properties)
                    self._register(properties)

    @property
    def address(self):
        return self._adapter.address

    @property
    def address_type(self):
        return self._adapter.address_type

    @property
    def name(self):
        return self._adapter.name

    @property
    def alias(self):
        return self._adapter.alias
