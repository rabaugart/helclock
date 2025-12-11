#!/usr/bin/env python3

import time
import c3

s = c3.Spi()

while True:
    s.putcolors([c3.ROT]*20)
    time.sleep(1.0)
    s.putcolors([c3.BLAU]*20)
    time.sleep(1.0)
    s.putcolors([c3.GRÜN]*20)
    time.sleep(1.0)
