#!/usr/bin/env python3

import time, sys
import c3

s = c3.Spi()

SL = 15

#s.putcolors([c3.BLAU]*SL)

def rotate(ba):
    return [ba[-1]] + ba[:-1]

def filled_color_array(cols,le,fillcolor=c3.SCHWARZ):
    return cols + [fillcolor]*(le-len(cols))

#sys.exit(0)

ca = filled_color_array( [c3.ROT,c3.GRÜN,c3.BLAU], SL )
ca = ([c3.ROT,c3.GRÜN,c3.BLAU]+[c3.SCHWARZ]*2)*3
ca = ([c3.GRÜN*0.3,c3.GRÜN,c3.GRÜN*0.3]+[c3.SCHWARZ]*2)*3

s.putcolors([c3.SCHWARZ]*SL)

while True:
    s.putcolors(ca)
    time.sleep(0.5)
    ca = rotate(ca)
    continue
    s.putcolors([c3.ROT]*SL)
    time.sleep(1.0)
    s.putcolors([c3.BLAU]*SL)
    time.sleep(1.0)
    s.putcolors([c3.GRÜN]*SL)
    time.sleep(1.0)
