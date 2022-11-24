# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

class RegistrationError(RuntimeError):
    def __init__(self, path, error):
        super().__init__(f'Registering {path} failed: {error}')
