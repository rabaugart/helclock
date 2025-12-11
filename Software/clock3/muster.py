#!/usr/bin/env python3

import time, sys
import c3

s = c3.Spi()

l = 20

#s.putcolors([c3.BLAU]*l)

#sys.exit(0)
while True:
    s.putcolors([c3.ROT]*l)
    time.sleep(1.0)
    s.putcolors([c3.BLAU]*l)
    time.sleep(1.0)
    s.putcolors([c3.GRÜN]*l)
    time.sleep(1.0)
