#!/usr/bin/env python

import spidev, time

spi = spidev.SpiDev()

spi.open(0,0)

spi.max_speed_hz = 1000000
#spi.mode = 0
#spi.bits_per_word = 8
spi.lsbfirst = False

class Color:
    def __init__(self,r,g,b):
        self.b = bytearray([r,g,b])

    def send(self):
        print(f"Sending {self.b}")
        spi.xfer2(self.b)

blau = Color(0,0,0xFF)
rot = Color(0xFF,0,0x00)

blau.send()

time.sleep(1.0)

rot.send()

spi.close()
