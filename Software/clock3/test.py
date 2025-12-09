#!/usr/bin/env python3

import datetime
import c3
import unittest

class T3(unittest.TestCase):

    def testTernär(self):
        self.assertEqual( c3.ternär(0), [0])
        self.assertEqual( c3.ternär(0,3), [0,0,0])
        self.assertEqual( c3.ternär(3), [0,1])
        self.assertEqual( c3.ternär(3,4), [0,1,0,0])
        self.assertEqual( c3.ternär(10), [1,0,1])
        self.assertEqual( c3.ternär(23), [2,1,2])
        self.assertEqual( c3.ternär(27), [0,0,0,1])
        self.assertEqual( c3.ternär(59), [2,1,0,2])
        t = datetime.time(5,37,2)
        l = c3.time_ternär_colors(t)
        self.assertEqual(len(l),11)
        self.assertEqual(l[:3],[c3.ROT,c3.GRÜN,c3.BLAU])
        self.assertEqual(l,[c3.ROT,c3.GRÜN,c3.BLAU,c3.GRÜN,c3.GRÜN,c3.ROT,c3.GRÜN,c3.ROT,c3.ROT,c3.ROT,c3.BLAU])
        self.assertEqual(c3.colors_bytes([c3.ROT,c3.GRÜN]),bytearray.fromhex("FF 00 00 00 FF 00"))
    def testColor(self):
        self.assertEqual(c3.ROT.b,bytearray([255,0,0]))
        self.assertEqual(c3.ternär_colors(0),[c3.ROT])
        self.assertEqual(c3.ternär_colors(10),[c3.GRÜN,c3.ROT,c3.GRÜN])
        self.assertEqual(c3.ternär_colors(10,4),[c3.ROT,c3.GRÜN,c3.ROT,c3.GRÜN])
        self.assertEqual(c3.ternär_colors(59),[c3.BLAU,c3.ROT,c3.GRÜN,c3.BLAU])
    def testSpi(self):
        s = c3.Spi()
        s.putcolors([c3.ROT,c3.BLAU])
        self.assertEqual(s.b,bytearray.fromhex("FF 00 00 00 00 FF"))
        t = datetime.time(17,23,3)
        l = c3.time_ternär_colors(t)
        self.assertEqual(len(l),11)
        self.assertEqual(l[0],c3.GRÜN)
        self.assertEqual(len(c3.colors_bytes(l)),33)
        s.putcolors(l)
        s.putcolors(c3.time_ternär_colors(t))
        s.puttime(datetime.datetime.now().time())
        self.assertEqual(len(s.b),33)

tl = unittest.TestLoader()
#tl.loadTestsFromModule(c3.hclock)
#tl.discover(".")
tl.loadTestsFromName("c3.hclock")
unittest.main(testLoader=tl,verbosity=2)
