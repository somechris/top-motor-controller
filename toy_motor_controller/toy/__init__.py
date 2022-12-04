# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .. import __version__

from .akogd_power_functions import AkogdPowerFunctionsHub
from .akogd_power_functions import AkogdPowerFunctionsRemoteControl
from .playmobil_rc_racers import PlaymobilRcRacersRemoteControl
from .playmobil_rc_racers import PlaymobilRcRacersVehicle


__all__ = (
    AkogdPowerFunctionsHub,
    AkogdPowerFunctionsRemoteControl,
    PlaymobilRcRacersRemoteControl,
    PlaymobilRcRacersVehicle,
)

__version__ = __version__
