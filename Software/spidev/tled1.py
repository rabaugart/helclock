#!/usr/bin/env python

import spidev, time

spi = spidev.SpiDev()

spi.open(0,0)

spi.max_speed_hz = 8000000
spi.mode = 0
spi.bits_per_word = 8
spi.lsbfirst = False

to_send = bytearray.fromhex("FF 00 00")
print(to_send)

spi.xfer(to_send)

time.sleep(1.0)

to_send = b'\x00\xFF\x00'

#spi.xfer2(to_send)

spi.close()

