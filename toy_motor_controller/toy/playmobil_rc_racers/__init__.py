# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .. import __version__

from .base import PlaymobilRcRacersBase
from .remote_control import PlaymobilRcRacersRemoteControl
from .vehicle import PlaymobilRcRacersVehicle


__all__ = (
    PlaymobilRcRacersBase,
    PlaymobilRcRacersRemoteControl,
    PlaymobilRcRacersVehicle,
    )

__version__ = __version__
