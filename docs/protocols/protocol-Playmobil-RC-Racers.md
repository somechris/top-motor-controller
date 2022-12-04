# Playmobil RC Racers communication protocol

This document describes the communication protocol of "Playmobil RC Racers" cars
and remote controls.



#### Table of Contents

1. [Supported devices](#supported-devices)
1. [Protocol](#protocol)
    1. [Advertisements](#advertisements)
    1. [Commands](#commands)
1. [Source](#source)



## Supported devices

This protocol is known to be valid for:

| Name | Link | Last seen on |
| --- | --- | --- |
| Playmobil 9089 - RC-Supersport-Racer | https://www.amazon.de/dp/B01M20S3MK | 2022-10-28 |
| Playmobil:THE MOVIE 70078 Rex Dasher's Porsche Mission E, Ab 6 Jahren  | https://www.amazon.de/dp/B07P7KKCNS | 2022-10-28 |

Due to similarity in form and function, this protocol is probably also valid
for:

| Name | Link | Last seen on |
| --- | --- | --- |
| PLAYMOBIL Action 9090 RC-Rocket-Racer mit Bluetooth-Steuerung, Ab 6 Jahren [Exklusiv bei Amazon] | https://www.amazon.de/dp/B01M11HLLM | 2022-10-28 |
| PLAYMOBIL® 70765 Porsche Mission E | https://www.amazon.de/dp/B08KTNWCWM | 2022-10-28 |
| Playmobil 9091 - RC-Rock'n'Roll-Racer | https://www.amazon.de/dp/B01LX4TJJJ | 2022-10-28 |



## Protocol

The cars start a [BLE advertisement](#advertisements) offering a specific
characteristic. Writing [commands](#commands) to this characteristic controls
the car.



### Advertisements

The advertisements of this protocol are done by the car.
They typically come from Bluetooth addresses starting in `AC:9A:22`, have a
local name (type `0x09`) starting in `PM-RC `, and characteristic
`06d1e5e7-79ad-4a71-8faa-373789f7d93c`.
Writing [commands](#commands) to this characteristic controls the car.



### Commands

Each command written to the [protocol's characteristic](#advertisements) is of
the following form:

```
+------+-------+------+
| TYPE | VALUE | 0x0f |
+------+-------+------+
````

where `TYPE` can only have the following four values:

| `TYPE` | Gist | Description |
| --- | --- | --- |
| `0x23` | speed | `VALUE` controls the speed of the car. `0x00` is full backwards, `0xff` is full forward. Values in between are possible (e.g.: `0xff` is faster forward than `0xb0`). How fast full forward/backward is, can be adjusted through the speed multiplier (see `0x25` below). The dead spot is affected by the speed multiplier as well. It's `0x20-0xd0` for speed multiplier `0x01` down to `0x70-0x90` for speed multiplier `0x05`. The speed set by this command gets reset after ~0.3s. So to keep the car moving, one has to issue this command about 4 times a second. |
| `0x24` | light | If `VALUE` is `0x01`, the light gets turned on. If it is `0x02`, it gets turned off. |
| `0x25` | speed multiplier | `VALUE` controls how fast the car's full speed (see `0x23` above) is. `0x01` is slowest, `0x05` is fastest. |
| `0x40` | steering | `VALUE` controls the direction the car steers to. `0x00` turns left, `0xff` turns right. Values in between are possible (`0xf0` steers farther to the right than `0xa0`). There does not seem to be a dead spot (other then the wiggle room of the steering mechanism itself). |



## Source

The main part got sourced from https://github.com/tmonjalo/playmobil-racer/blob/main/protocol.md .