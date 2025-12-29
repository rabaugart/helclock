#!/usr/bin/env python3

import datetime
import c3, c3.gen, c3.hclock
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
        self.assertEqual(c3.ROT,c3.Color(255,0,0))
        self.assertEqual(c3.RGB.rot.value,0)
        self.assertEqual(c3.RGB.grün.value,1)
        self.assertEqual(c3.RGB.blau.value,2)
        c = c3.Color(10,10,10)
        c.set(c3.RGB.blau,200)
        self.assertEqual(c.b,bytearray([10,10,200]))
        self.assertEqual((c3.ROT*0.5).b,bytearray([127,0,0]))
        self.assertEqual((c3.ROT*1.5).b,bytearray([255,0,0]))
        self.assertEqual((c3.ROT*-1.5).b,bytearray([0,0,0]))
        self.assertEqual((c3.WEISS*0.5).b,bytearray([127,127,127]))
        self.assertEqual((c3.WEISS*"0.5").b,bytearray([127,127,127]))
        self.assertEqual(c3.WEISS.msg_dict(),{"rot":255,"grün":255,"blau":255})
        self.assertRaises(ValueError,lambda: c3.ROT*"hallo")
        self.assertEqual(c3.ternär_colors(0),[c3.ROT])
        self.assertEqual(c3.ternär_colors(10),[c3.GRÜN,c3.ROT,c3.GRÜN])
        self.assertEqual(c3.ternär_colors(10,4),[c3.ROT,c3.GRÜN,c3.ROT,c3.GRÜN])
        self.assertEqual(c3.ternär_colors(59),[c3.BLAU,c3.ROT,c3.GRÜN,c3.BLAU])
    def testSpi(self):
        s = c3.Spi()
        s.putcolors([c3.ROT,c3.BLAU])
        self.assertEqual(s.bs[0],bytearray.fromhex("FF 00 00 00 00 FF"))
    def testSpiZeit(self):
        s = c3.Spi()
        t = datetime.time(17,23,3)
        l = c3.time_ternär_colors(t)
        self.assertEqual(len(l),11)
        self.assertEqual(l[0],c3.GRÜN)
        self.assertEqual(len(c3.colors_bytes(l)),33)
        s.putcolors(l)
        s.putcolors(c3.time_ternär_colors(t))
        s.puttime(datetime.datetime.now().time())
        self.assertEqual(len(s.bs[0]),33)
    def testGenerator(self):
        s = c3.Spi()
        s.putcolgen(testiter(1),0.01)
        self.assertEqual(len(s.bs),2)
        self.assertEqual(s.bs[0],c3.colors_bytes([c3.ROT,c3.ROT]))
        self.assertEqual(s.bs[1],c3.colors_bytes([c3.GRÜN,c3.GRÜN]))
    def testGeneratorRotate(self):
        s = c3.Spi()
        s.putcolgen(c3.gen.take(c3.gen.rotate([c3.ROT,c3.GRÜN]),3),sleep=0.01)
        self.assertEqual(len(s.bs),3)
        self.assertEqual(s.bs[0],c3.colors_bytes([c3.ROT,c3.GRÜN]))
        self.assertEqual(s.bs[2],c3.colors_bytes([c3.ROT,c3.GRÜN]))
    def testGeneratorRotate2(self):
        self.assertEqual(c3.gen.steplist(3),[0,1,2,3,2,1])
        s = c3.Spi()
        s.putcolgen(c3.gen.take(c3.gen.blink([c3.ROT,c3.GRÜN],3),3),sleep=0.01)
        self.assertEqual(len(s.bs),3)
        self.assertEqual(s.bs[0],c3.colors_bytes([c3.ROT*0.0,c3.GRÜN*0.0]))
        self.assertEqual(s.bs[1],c3.colors_bytes([c3.ROT*(1/3.0),c3.GRÜN*(1/3.0)]))
        self.assertEqual(s.bs[2],c3.colors_bytes([c3.ROT*(2/3.0),c3.GRÜN*(2/3.0)]))
    def testGeneratorHClock(self):
        s = c3.Spi()
        s.putcolgen(c3.gen.take(c3.hclock.zeit_spi_generator(),1),sleep=0.01)
        self.assertEqual(len(s.bs[0]),c3.hclock.NROWS*c3.hclock.NCOLS*3)

def testiter(n):
    for i in [c3.ROT,c3.GRÜN]*n:
        yield [i,i]
