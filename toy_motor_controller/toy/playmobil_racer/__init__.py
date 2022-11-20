# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .. import __version__

from .remote_control import PlaymobilRacerRemoteControl
from .vehicle import PlaymobilRacerVehicle


__all__ = (
    PlaymobilRacerRemoteControl,
    PlaymobilRacerVehicle,
    )

__version__ = __version__
