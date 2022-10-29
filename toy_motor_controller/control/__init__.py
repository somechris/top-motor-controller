# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

from .. import __version__

__version__ = __version__


def create_control_property(control_class):
    def described_control(description='', *args, **kwargs):
        def inner(setter):
            control = control_class(setter, *args, **kwargs)
            return property(
                fget=control.get,
                fset=control.set,
                doc=description)
        return inner
    return described_control


from .control import Control

from .standardized_control import StandardizedControl
standardized_control = create_control_property(StandardizedControl)

from .boolean_standardized_control import BooleanStandardizedControl
boolean_standardized_control = create_control_property(
    BooleanStandardizedControl)

from .min_max_standardized_control import MinMaxStandardizedControl
min_max_standardized_control = create_control_property(
    MinMaxStandardizedControl)

from .min_max_int_standardized_control import MinMaxIntStandardizedControl
min_max_int_standardized_control = create_control_property(
    MinMaxIntStandardizedControl)

from .uint8_standardized_control import UInt8StandardizedControl
uint8_standardized_control = create_control_property(UInt8StandardizedControl)

__all__ = (
    create_control_property,
    Control,
    standardized_control,
    StandardizedControl,
    boolean_standardized_control,
    BooleanStandardizedControl,
    min_max_standardized_control,
    MinMaxStandardizedControl,
    min_max_int_standardized_control,
    MinMaxIntStandardizedControl,
    uint8_standardized_control,
    UInt8StandardizedControl,
)
