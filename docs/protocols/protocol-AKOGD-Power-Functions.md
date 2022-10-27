# AKOGD Power Functions communication protocol

This document describes the communication protocol of "AKOGD Technik Power
Functions", which is a set of remote control, hub, and motors compatible with
common interlocking brick toys.



#### Table of Contents

1. [Supported devices](#supported-devices)
1. [Protocol](#protocol)
    1. [Advertisements](#advertisements)
    1. [`STAT` values](#stat-values)
    1. [`MX` values](#mx-values)
    1. [Software remote controls](#software-remote-controls)
    1. [Hardware remote controls](#hardware-remote-controls)
    1. [Hubs](#hubs)
1. [Source](#source)



## Supported devices

This protocol is known to be valid for:

| Name | Link | Last seen on |
| --- | --- | --- |
| AKOGD Technik Power Functions, Technik motoren Set, Technik Batteriebox Set, 8 Teile Kompatibel mit Lego Technic | https://www.amazon.de/dp/B09J8HTTQW/ | 2022-10-27 |
| AKOGD Power Functions Set, Motoren Set mit Motor, Fernbedienung, Batteriebox, M/L-Motor, Extension Wire Kompatibel mit vielen Modellen (#4) | https://www.amazon.de/dp/B09M3QFPSZ/ | 2022-10-27 |


Due to similarity in form and function, this protocol is probably also valid
for:

| Name | Link | Last seen on |
| --- | --- | --- |
| AKOGD Power Functions Set, Motoren Set mit Motor, Fernbedienung, Batteriebox, LED, Extension Wire Kompatibel mit vielen Modellen (#5) | https://www.amazon.de/dp/B09M3LSN5X/ | 2022-10-27 |
| AKOGD Power Functions Set, Motoren Set mit Motor, Fernbedienung, Batteriebox, Servomotor, L-Motor Kompatibel mit vielen Modellen (#1) | https://www.amazon.de/dp/B09M3NM52R/ | 2022-10-27 |
| AKOGD Power Functions Set, Motoren Set mit Motor, Fernbedienung, Batteriebox, Servomotor, LED, Extension Wire, L-Motor Kompatibel mit vielen Modellen | https://www.amazon.de/dp/B09N2PFNKN/ | 2022-10-27 |
| AKOGD Power Functions Set, Motoren Set mit Motor, Fernbedienung, Batteriebox, Servomotor, XL-Motor Kompatibel mit vielen Modellen (#2)  | https://www.amazon.de/dp/B09M3L678Q/ | 2022-10-27 |
| AKOGD Power Functions Set, Motoren Set mit Motor, Fernbedienung, Batteriebox, XL/M-Motor Kompatibel mit vielen Modellen (#3) | https://www.amazon.de/dp/B09M3LBTB4/ | 2022-10-27 |
| Bybo Technik Power Functions, Technik motoren Set, Technik Batteriebox Set, 4 Teile Kompatibel mit Lego Technic | https://www.amazon.de/dp/B095YTYFYX/ | 2022-10-27 |
| Bybo Technik Power Functions, Technik motoren Set, Technik Batteriebox Set, 8 Teile Kompatibel mit Lego Technic | https://www.amazon.de/dp/B095YBHRDC/ | 2022-10-27 |
| Bybo Technik Power Functions, Technik motoren Set, Technik Batteriebox Set, 8 Teile Kompatibel mit Lego Technic | https://www.amazon.de/dp/B095YL94BW/ | 2022-10-27 |
| WWEI Technik Power Functions Kit, 11 Stück Motoren Fernbedienung Akku für Technik Autos, Kompatibel mit Lego Technic | https://www.amazon.de/dp/B09F9S7VJG/ | 2022-10-27 |
| WWEI Technik Power Functions Kit, 6 Stück Motoren Fernbedienung Akku für Technik Autos, Kompatibel mit Lego Technic | https://www.amazon.de/dp/B09F9R5BMV/ | 2022-10-27 |
| WWEI Technik Power Functions Kit, 8 Stück Motoren Fernbedienung Akku für Technik Autos, Kompatibel mit Lego Technic | https://www.amazon.de/dp/B09F9SL7Z6/ | 2022-10-27 |
| WWEI Technik Power Functions Kit, 8 Stück Motoren Fernbedienung Beleuchtungsset Akku für Technik Autos, Kompatibel mit Lego Technic | https://www.amazon.de/dp/B09F9S5YKJ/ | 2022-10-27 |



## Protocol

Endpoints find each other by setting up a Bluetooth LE advertisement
and looking for other Bluetooth LE advertisements. Values of the
switches on the remote controls are not sent to the hub, but broadcast
via advertisements as well.



### Advertisements

The advertisements for this protocol lack local names and other
properties. They only come with 21 bytes of manufacturer data (i.e.:
type `0xff`) and have the following form:

```
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
| 00 | 00 | 67 |STAT| R1 | R2 | R3 | H1 | H2 | H3 | MA | MB | MC | MD | 00 | 00 | 00 | 00 | 00 | 00 | CK |
+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+

(all numbers are hexadecimal)
```

where

* `STAT` is the status of the endpoint (see [`STAT` values](#stat-values)
  below).
* `H1`, `H2`, `H3` are three bytes that identify a hub
* `R1`, `R2`, `R3` are three bytes that identify a remote control
* `M1`, `M2`, `M3`, `M4` are the values for the four motor outputs (see
    [`Mx` values](#mx-values) below). `MA` maps to the output `A` on
    the hub, `MB` to `B`, `MC` to `C`, and `MD` to `D`.

* `CK` is a checksum that starts with value `0xe9` and then `XOR`s the first
    20 bytes of the data.



### `STAT` values

* `0x01`: Software remote control flagging its availability to hubs.
* `0x02`: Software remote control sending data to hub.
* `0x03`: Hardware remote control flagging its availability to hubs.
* `0x04`: Hardware remote control sending data to hub.
* `0x05`: Hub flagging to a remote control that it is accepting data.



### `Mx` values:

`0x80` means neutral.

`0x00` rotates full-speed clockwise (looking at the front of the motor).

`0xff` rotates full speed counter-clockwise (looking at the front of the
    motor).

Any values from 0x00 to `0xff` are possible (e.g.: `0xee` yields a slower
clockwise rotation than `0xff`).

There is a dead spot between around `0x60` and `0xa0`. But the edges of that
dead spot are neither crisp not consistent between hubs and motors.



### Software remote controls

Software remote controls do not need to have static Bluetooth address. They
can vary with each update of the outputs.

1. The software remote control picks `R1`, `R2`, `R3` at random.

2. The software remote control start an advertisement with `STAT` `0x01` and
    `H1`, `H2`, `H3`, `MA`, `MB`, `MC`, `MD` all `0x00`.

3. Once a hub wants to flag to the remote control that it is accepting input,
    the hub starts an advertisement with `STAT` `0x05`, `R1`, `R2`, `R3` from
    the remote control and with its own `H1`, `H2`, `H3`, and `MA`, `MB`,
    `MC`, `MD` all `0x00`.

4. The software remote control updates its advertisement data. `STAT` becomes
    `0x02`, and `H1`, `H2`, `H3` from the hub get used. And `MA`, `MB`, `MC`,
    `MD` get set to the desired motor outputs. The advertisement stays on, and
    gets updated whenever a change in motor outputs should change.

5. The hub's blue light switches from blinking to constant on to show that it
    is connected.



### Hardware remote controls

Hardware remote controls seem to have a Bluetooth address of
`C0:00:00:R3:R2:R1`. The address does not change.

2. The software remote control start an advertisement with `STAT` `0x03` and
    `H1`, `H2`, `H3`, `MA`, `MB`, `MC`, `MD` all `0x00`.

3. Once a hub wants to flag to the remote control that it is accepting input,
    the hub starts an advertisement with `STAT` `0x05`, `R1`, `R2`, `R3` from
    the remote control and with its own `H1`, `H2`, `H3`, and `MA`, `MB`,
    `MC`, `MD` all `0x00`.

4. The hardware remote control updates its advertisement data. `STAT` becomes
    `0x04`, and `H1`, `H2`, `H3` from the hub get used. And `MA`, `MB`, `MC`,
    `MD` get set to the desired motor outputs. The advertisement stays on, and
    gets updated whenever a change in motor outputs should change.

5. The hub's blue light and the hardware remote control's red light switch
    from blinking to constant on to show that they are connected.



### Hubs

Hubs seem to have a Bluetooth address of `C0:00:00:H3:H2:H1`. The
address does not change.

When a hub wants to flag that it is accepting input from a remote, the hub
starts an advertisement with `STAT` `0x05`, and `R1`, `R2`, 'R3` from the
remote control that it wants input from.

Once the remote control offers motor data in its advertisement, the hub shuts
down its advertisement again.



## Source

The protocol was analyzed by simply scanning for Bluetooth LE advertisements.
