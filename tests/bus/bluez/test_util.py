# This file is part of toy-motor-controller and licensed under the
# GNU Affero General Public License v3.0 only (See LICENSE.txt)
# SPDX-License-Identifier: AGPL-3.0-only

import dbus

from tests import BasicTestCase

from toy_motor_controller.bus.bluez import \
    convert_device_object_path_to_mac_address
from toy_motor_controller.bus.bluez import normalize_io_options


class UtilTestCase(BasicTestCase):
    def test_convert_device_object_path_to_mac_address_None(self):
        self.assertIsNone = convert_device_object_path_to_mac_address(None)

    def test_convert_device_object_path_to_mac_address_plain(self):
        object_path = dbus.ObjectPath('/org/bluez/hci0/dev_AB_de_01_fC_23_cF')
        actual = convert_device_object_path_to_mac_address(object_path)
        self.assertEqual(actual, 'ab:de:01:fc:23:cf')

    def test_normalize_io_options_plain(self):
        options = dbus.Dictionary({
                dbus.String('device'): dbus.ObjectPath(
                    '/org/bluez/hci0/dev_AB_CD_EF_01_23_45', variant_level=1),
                dbus.String('offset'): dbus.UInt16(42, variant_level=1),
                dbus.String('link'): dbus.String('LE', variant_level=1),
                dbus.String('mtu'): dbus.UInt16(23, variant_level=1),
                dbus.String('type'): dbus.String('foo', variant_level=1),
                }, signature=dbus.Signature('sv'))
        actual = normalize_io_options(options)
        self.assertEqual(actual, {
                'address': 'ab:cd:ef:01:23:45',
                'offset': 42,
                'link': 'LE',
                'mtu': 23,
                'type_': 'foo',
                })

    def test_normalize_io_options_None_dict(self):
        options = None
        actual = normalize_io_options(options)
        self.assertEqual(actual, {
                'address': None,
                'offset': None,
                'link': None,
                'mtu': None,
                'type_': None,
                })

    def test_normalize_io_options_missing_all_values(self):
        options = dbus.Dictionary({}, signature=dbus.Signature('sv'))
        actual = normalize_io_options(options)
        self.assertEqual(actual, {
                'address': None,
                'offset': None,
                'link': None,
                'mtu': None,
                'type_': None,
                })

    def test_normalize_io_options_missing_some_values(self):
        options = dbus.Dictionary({
                dbus.String('device'): dbus.ObjectPath(
                    '/org/bluez/hci0/dev_AB_CD_EF_01_23_45', variant_level=1),
                dbus.String('mtu'): dbus.UInt16(23, variant_level=1),
                }, signature=dbus.Signature('sv'))
        actual = normalize_io_options(options)
        self.assertEqual(actual, {
                'address': 'ab:cd:ef:01:23:45',
                'offset': None,
                'link': None,
                'mtu': 23,
                'type_': None,
                })
