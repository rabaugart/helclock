#!/usr/bin/env python

import spidev, time

spi = spidev.SpiDev()

spi.open(0,0)

spi.max_speed_hz = 2000000
#spi.mode = 1
#spi.bits_per_word = 8
#spi.lsbfirst = False

länge = 11

class Color:
    def __init__(self,r,g,b):
        self.b = bytearray([r,g,b])

    def sendn(self,n=länge,sleep=1.0):
        spi.writebytes(self.b*n)
        if sleep:
            time.sleep(sleep)

    def send(self,sleep=None):
        print(f"Sending {self.b}")
        spi.writebytes(self.b)
        #spi.xfer(self.b,1000000, 1)
        if sleep:
            time.sleep(sleep)

blau = Color(0,0,0xFF)
rot = Color(0xFF,0x00,0x00)
grün = Color(0x00,0xFF,0X00)
schwarz = Color(0,0,0)
weiss = Color(0xFF,0xFF,0xFF)
gelb = Color(0xFF,0xFF,0x00)

while True:
    blau.sendn()
    rot.sendn()
    grün.sendn()
    weiss.sendn()
    gelb.sendn()
    spi.writebytes((blau.b+rot.b+grün.b)*4)
    time.sleep(1)
    spi.writebytes(schwarz.b*11)
    time.sleep(1)

spi.close()
