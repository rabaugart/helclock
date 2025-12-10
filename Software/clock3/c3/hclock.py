import math, re, functools
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

STAMM_RE = re.compile("^([^_]+).*$",re.U)

def wort_stamm(w):
    "Entferne _A, _B"
    m = STAMM_RE.match(w.name)
    assert(m)
    return m.groups()[0]

def wort_koordinaten(w):
    l = [ (i,t) for (i,(t,l)) in enumerate(TEXT) if w in l ]
    assert(len(l)==1)
    (row,t) = l[0]
    ws = wort_stamm(w)
    col = t.find(ws)
    assert(col>=0)
    return [(row,col+i) for i in range(len(ws))]

#
# Indexe:
# Col   0   1   2 ..  9   10
#       ⬆  ⬇  ⬆     ⬇   ⬆
# r0    9  10  29 .. 90  109
# r1    8  11  28 .. 91  108
# r.   ..  ..  .. .. ..
# r.   ..  ..  .. .. ..   ..
# r8    1  18  21 .. 98  101
# r9    0  19  20 .. 99  100
#
# (0,0) -> 10
# (1,0) ->  9
# (10,0) -> 0
# (0,1) -> 11

def koordinaten_index(r,c):
    "Index für ein Koordinatenpaar"
    return (c+1)*10-r-1 if c % 2 == 0 else c*10+r

# Die im Satz zu nutzende Stunde
S = Enum('Stunde',["DIESE","NÄCHSTE"])

# Satzfragmente in Abhängigkeit von der Minute
# "ES IST"  und "UHR" fehlen und müssen immer dazu gesetzt werden
SATZ_INDEX = [
    [S.DIESE], # Minute 0..5
    [W.FÜNF_A, W.NACH, S.DIESE], # Minute 5..10
    [W.ZEHN_A, W.NACH, S.DIESE], # ...
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
    "Finde den Index für das Satzfragment zur Uhrzeit anhand der Minute"
    return math.floor(ti.minute*len(SATZ_INDEX)/60.0)

def satz_vorlage(ti):
    "Satzvorlage mit Stundenplatzhalter zur Uhrzeit"
    return [W.ES,W.IST] + SATZ_INDEX[satz_index(ti)] + [W.UHR]

# Stundenworte zur Stunde
STUNDEN = [W.ZWÖLF,W.EINS,W.ZWEI,W.DREI_B,W.VIER,W.FÜNF_B,W.SECHS,W.SIEBEN,W.ACHT,W.NEUN,W.ZEHN_B,W.ELF]

def stundenwort(st):
    "Stundenwort zur Stunde"
    return STUNDEN[st % len(STUNDEN)]

def ersetze_stunde(wort,ti):
    "Ersetze S.DIESE/S.NÄCHSTE durch Stundenwort"
    if wort == S.DIESE:
        return stundenwort(ti.hour)
    if wort == S.NÄCHSTE:
        return stundenwort(ti.hour+1)
    return wort

def satz(ti):
    "Vollständiger Satz zur Urzeit"
    return [ersetze_stunde(w,ti) for w in satz_vorlage(ti)]

def wort_indexe(w):
    "Tupel mit allen Indexen für ein Wort: (w,[i0,i1...])"
    return (w,[koordinaten_index(*k) for k in wort_koordinaten(w)])

class HTest(unittest.TestCase):
    def testWort(self):
        self.assertEqual(W.ACHT.name,"ACHT")
        self.assertEqual(wort_stamm(W.ACHT),"ACHT")
        self.assertEqual(wort_stamm(W.ZEHN_A),"ZEHN")
        self.assertEqual(wort_stamm(W.ZWÖLF),"ZWÖLF")
        self.assertEqual(wort_stamm(W.FÜNF_A),"FÜNF")
    def testKoordinaten(self):
        self.assertEqual(wort_koordinaten(W.ES),[(0,0),(0,1)])
        self.assertEqual(wort_koordinaten(W.FÜNF_A),[(0,7),(0,8),(0,9),(0,10)])
        self.assertEqual(wort_koordinaten(W.ACHT),[(7,7),(7,8),(7,9),(7,10)])
    def testKoordinatenIndex(self):
        self.assertEqual(koordinaten_index(0,0),9)
        self.assertEqual(koordinaten_index(9,0),0)
        self.assertEqual(koordinaten_index(0,1),10)
        self.assertEqual(koordinaten_index(9,1),19)
        self.assertEqual(koordinaten_index(0,10),109)
        self.assertEqual(koordinaten_index(9,10),100)
    def testWortIndexe(self):
        self.assertEqual(wort_indexe(W.ES), (W.ES,[9,10]))
        self.assertEqual(wort_indexe(W.UHR), (W.UHR,[80,99,100]))
        self.assertEqual(wort_indexe(W.FÜNF_A), (W.FÜNF_A,[70,89,90,109]))
        self.assertEqual(wort_indexe(W.ZEHN_B), (W.ZEHN_B,[0,19,20,39]))
    def testKonsistenz(self):
        # Jedes Wort wird in einer Zeile erwähnt
        l = sum((wl for (_,wl) in TEXT), [])
        so = lambda l:l.sort(key=lambda w:w.name)
        self.assertEqual(so(l),so(list(W)))
        # Jedes Wort kommt im Text vor
        fulltext = " ".join(  t for (t,_) in TEXT )
        self.assertEqual( list(w for w in list(W) if fulltext.find(wort_stamm(w)) < 0), [])
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
    def testZeitSatz(self):
        self.assertEqual(satz(time(11,4,59)),[W.ES,W.IST,W.ELF,W.UHR])
        self.assertEqual(satz(time(11,5,0)),[W.ES,W.IST,W.FÜNF_A,W.NACH,W.ELF,W.UHR])
        self.assertEqual(satz(time(11,10)),[W.ES,W.IST,W.ZEHN_A,W.NACH,W.ELF,W.UHR])
        self.assertEqual(satz(time(11,15)),[W.ES,W.IST,W.VIERTEL,W.NACH,W.ELF,W.UHR])
        self.assertEqual(satz(time(11,54,59)),[W.ES,W.IST,W.ZEHN_A,W.VOR,W.ZWÖLF,W.UHR])
        self.assertEqual(satz(time(11,55)),[W.ES,W.IST,W.FÜNF_A,W.VOR,W.ZWÖLF,W.UHR])
        self.assertEqual(satz(time(11,59,59)),[W.ES,W.IST,W.FÜNF_A,W.VOR,W.ZWÖLF,W.UHR])
        self.assertEqual(satz(time(23,0)),[W.ES,W.IST,W.ELF,W.UHR])
