#!/usr/bin/env python

import spidev, time

spi = spidev.SpiDev()

spi.open(0,0)

spi.max_speed_hz = 8000000
spi.mode = 0
spi.bits_per_word = 8
spi.lsbfirst = False

class Color:
    def __init__(self,r,g,b):
        self.b = bytearray([r,g,b])

    def send(self):
        spi.xfer(self.b)

blau = Color(0,0,0xFF)
rot = Color(0xFF,0,0x0F)

to_send = bytearray.fromhex("FF 00 00")
print(to_send)

blau.send()
#spi.xfer(to_send)

time.sleep(1.0)

to_send = b'\x00\xFF\x00'

#spi.xfer2(to_send)


rot.send()
#spi.xfer2(to_send)

spi.close()
