# AKOGD Power Functions communication protocol

![Software remote control](images/software-remote-control-100px.jpg)
![Remote control](images/remote-control-100px.jpg)
![Hub](images/hub-100px.jpg)

This document describes the communication protocol of [AKOGD Power
Functions](README.md), which is are remote controls, and hubs that
allow to connect motors, and are structurally compatible with common
interlocking brick toys.

This document is the basis for the [AKOGD Power Functions
implementation in Toy Motor Controller](README.md).

#### Contents

1. [Overview](#protocol)
1. [Bluetooth advertisements](#bluetooth-advertisements)
1. [`STAT` values](#stat-values)
1. [`MX` values](#mx-values)
1. [Software remote controls](#software-remote-controls)
1. [Hardware remote controls](#hardware-remote-controls)
1. [Hubs](#hubs)
1. [Source](#source)



## Protocol

Devices find each other by setting up a [Bluetooth LE
advertisement][#advertisements] and looking for other Bluetooth LE
advertisements. Values of the switches on the remote controls are not
sent to the hub through GATT, but through advertisements as well.



## Bluetooth advertisements

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

* `STAT` is the status of the device (see [`STAT` values](#stat-values)
  below).
* `H1`, `H2`, `H3` are three bytes that identify a hub
* `R1`, `R2`, `R3` are three bytes that identify a remote control
* `M1`, `M2`, `M3`, `M4` are the values for the four motor outputs (see
    [`Mx` values](#mx-values) below). `MA` maps to the output `A` on
    the hub, `MB` to `B`, `MC` to `C`, and `MD` to `D`.

* `CK` is a checksum that starts with value `0xe9` and then `XOR`s the first
    20 bytes of the data.



## `STAT` values

* `0x01`: Software remote control flagging its availability to hubs.
* `0x02`: Software remote control sending data to hub.
* `0x03`: Hardware remote control flagging its availability to hubs.
* `0x04`: Hardware remote control sending data to hub.
* `0x05`: Hub flagging to a remote control that it is accepting data.



## `Mx` values:

`0x80` means neutral.

`0x00` means full-speed in one direction.

`0xff` means full-speed in the other direction.

Any values from `0x00` to `0xff` are possible (e.g.: `0xee` yields a slower
rotation than `0xff`).



## Software remote controls

![Software remote control](images/software-remote-control-100px.jpg)

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



## Hardware remote controls

![Remote control](images/remote-control-100px.jpg)

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



## Hubs

![Hub](images/hub-100px.jpg)

Hubs seem to have a Bluetooth address of `C0:00:00:H3:H2:H1`. The
address does not change.

When a hub wants to flag that it is accepting input from a remote, the hub
starts an advertisement with `STAT` `0x05`, and `R1`, `R2`, `R3` from the
remote control that it wants input from.

Once the remote control offers motor data in its advertisement, the hub shuts
down its advertisement again.

If the hub does not receive advertisements for ~2s, it sets all outputs to
neutral.



## Source

The protocol was analyzed by simply scanning for Bluetooth LE advertisements.
