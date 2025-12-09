import math
from datetime import time
import unittest

from enum import Enum

try:
    from .spi import Spi
except:
    from .tspi import Spi

W = Enum('W',"ES IST FÜNF_A ZEHN_A ZWANZIG DREI_A VIERTEL VOR NACH HALB \
ELF FÜNF_B EINS ZWEI DREI_B VIER SECHS ACHT SIEBEN ZWÖLF ZEHN_B NEUN UHR".split(" "))

TEXT = [
# 01234567890
("ESKISTAFÜNF", [ W.ES, W.IST, W.FÜNF_A ]), # 0
("ZEHNZWANZIG", [ W.ZEHN_A, W.ZWANZIG ]), # 1
("DREIVIERTEL", [ W.DREI_A, W.VIERTEL ]), # 2
("VORFUNKNACH", [ W.VOR, W.NACH ]), # 3
("HALBAELFÜNF", [ W.HALB, W.ELF, W.FÜNF_B ]), # 4
("EINSXAMZWEI", [ W.EINS, W.ZWEI ]), # 5
("DREIPMJVIER", [ W.DREI_B, W.VIER ]), # 6
("SECHSNLACHT", [ W.SECHS, W.ACHT ]), # 7
("SIEBENZWÖLF", [ W.SIEBEN, W.ZWÖLF ]), # 8
("ZEHNEUNKUHR", [ W.ZEHN_B, W.NEUN, W.UHR ]), # 9
]

S = Enum('Stunde',["DIESE","NÄCHSTE"])
# ES IST ....
SATZ_INDEX = [
    [S.DIESE],
    [W.FÜNF_A, W.NACH, S.DIESE],
    [W.ZEHN_A, W.NACH, S.DIESE],
    [W.VIERTEL, W.NACH, S.DIESE],
    [W.ZWANZIG, W.NACH, S.DIESE],
    [W.FÜNF_A, W.ZWANZIG, W.NACH, S.DIESE],
    [W.HALB, S.NÄCHSTE],
    [W.FÜNF_A, W.ZWANZIG, W.VOR, S.NÄCHSTE],
    [W.ZWANZIG, W.VOR, S.NÄCHSTE],
    [W.VIERTEL, W.VOR, S.NÄCHSTE],
    [W.ZEHN_A, W.VOR, S.NÄCHSTE],
    [W.FÜNF_A, W.VOR, S.NÄCHSTE],
]

def satz_index(ti):
    return math.floor(ti.minute*len(SATZ_INDEX)/60.0)

def satz_vorlage(ti):
    return [W.ES,W.IST] + SATZ_INDEX[satz_index(ti)]

STUNDEN = [W.ZWÖLF,W.EINS,W.ZWEI,W.DREI_B,W.VIER,W.FÜNF_B,W.SECHS,W.SIEBEN,W.ACHT,W.NEUN,W.ZEHN_B,W.ELF]

def stundenwort(st):
    return STUNDEN[st % len(STUNDEN)]

def ersetze_stunde(wort,ti):
    if wort == S.DIESE:
        return stundenwort(ti.hour)
    if wort == S.NÄCHSTE:
        return stundenwort(ti.hour+1)
    return wort

def satz(ti):
    return [ersetze_stunde(w,ti) for w in satz_vorlage(ti)]

class HTest(unittest.TestCase):
    def testIndex(self):
        self.assertEqual(satz_index(time(12,0)),0)
        self.assertEqual(satz_index(time(12,5)),1)
        self.assertEqual(satz_index(time(12,6)),1)
        self.assertEqual(satz_index(time(12,54)),10)
        self.assertEqual(satz_index(time(12,55)),11)
    def testStunde(self):
        self.assertEqual(stundenwort(0),W.ZWÖLF)
        self.assertEqual(stundenwort(1),W.EINS)
        self.assertEqual(stundenwort(11),W.ELF)
        self.assertEqual(stundenwort(12),W.ZWÖLF)
        self.assertEqual(stundenwort(13),W.EINS)
        self.assertEqual(stundenwort(14),W.ZWEI)
        self.assertEqual(stundenwort(23),W.ELF)
    def testZeit(self):
        self.assertEqual(satz(time(11,4,59)),[W.ES,W.IST,W.ELF])
        self.assertEqual(satz(time(11,5,0)),[W.ES,W.IST,W.FÜNF_A,W.NACH,W.ELF])
        self.assertEqual(satz(time(11,10)),[W.ES,W.IST,W.ZEHN_A,W.NACH,W.ELF])
        self.assertEqual(satz(time(11,15)),[W.ES,W.IST,W.VIERTEL,W.NACH,W.ELF])
        self.assertEqual(satz(time(11,54,59)),[W.ES,W.IST,W.ZEHN_A,W.VOR,W.ZWÖLF])
        self.assertEqual(satz(time(11,55)),[W.ES,W.IST,W.FÜNF_A,W.VOR,W.ZWÖLF])
        self.assertEqual(satz(time(11,59,59)),[W.ES,W.IST,W.FÜNF_A,W.VOR,W.ZWÖLF])
        self.assertEqual(satz(time(23,0)),[W.ES,W.IST,W.ELF])
