#!/usr/bin/env python

import spidev, time

spi = spidev.SpiDev()

spi.open(0,0)

spi.max_speed_hz = 2000000
#spi.mode = 1
#spi.bits_per_word = 8
#spi.lsbfirst = False

class Color:
    def __init__(self,r,g,b):
        self.b = bytearray([r,g,b])

    def send(self,sleep=None):
        print(f"Sending {self.b}")
        spi.writebytes(self.b)
        #spi.xfer(self.b,1000000, 1)
        if sleep:
            time.sleep(sleep)

blau = Color(0,0,0xFF)
rot = Color(0xFF,0x00,0x00)
grün = Color(0x00,0xFF,0X00)

while True:
    blau.send(1.0)
    rot.send(1.0)
    grün.send(1.0)

spi.close()
