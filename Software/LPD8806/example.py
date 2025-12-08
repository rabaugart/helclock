#!/usr/bin/python

from time import sleep
import LPD8806

led = LPD8806.strand(1)

on = True
while True:
    led.fill( (255 if on else 0), 0, 0)
    on = not on
    led.update()
    sleep(1.5)
