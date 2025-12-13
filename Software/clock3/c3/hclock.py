import math, re, functools, datetime, itertools
from datetime import time
import unittest

from .color import colors_bytes, SCHWARZ, ROT

from enum import Enum

try:
    from .spi import Spi
except:
    from .tspi import Spi

W = Enum('W',"ES IST FÜNF_A ZEHN_A ZWANZIG DREI_A VIERTEL VOR NACH HALB \
ELF FÜNF_B EIN EINS ZWEI DREI_B VIER SECHS ACHT SIEBEN ZWÖLF ZEHN_B NEUN UHR".split(" "))

TEXT = [
# 01234567890
("ESKISTAFÜNF", [ W.ES, W.IST, W.FÜNF_A ]), # 0
("ZEHNZWANZIG", [ W.ZEHN_A, W.ZWANZIG ]), # 1
("DREIVIERTEL", [ W.DREI_A, W.VIERTEL ]), # 2
("VORFUNKNACH", [ W.VOR, W.NACH ]), # 3
("HALBAELFÜNF", [ W.HALB, W.ELF, W.FÜNF_B ]), # 4
("EINSXAMZWEI", [ W.EIN, W.EINS, W.ZWEI ]), # 5
("DREIPMJVIER", [ W.DREI_B, W.VIER ]), # 6
("SECHSNLACHT", [ W.SECHS, W.ACHT ]), # 7
("SIEBENZWÖLF", [ W.SIEBEN, W.ZWÖLF ]), # 8
("ZEHNEUNKUHR", [ W.ZEHN_B, W.NEUN, W.UHR ]), # 9
]

def koordinaten_buchstabe(r,c):
    "Buchstabe an der Position r,c"
    return TEXT[r][0][c]

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

NROWS = 10
NCOLS = 11

#
# (0,0) -> 10
# (1,0) ->  9
# (10,0) -> 0
# (0,1) -> 11
#
# Indexe:
# Col   0   1   2 ..  9   10
#       ⬆  ⬇  ⬆     ⬇   ⬆
# r0  109  90  89 .. 10    9
# r1  108  91  88 .. 11    8
# r.   ..  ..  .. .. ..   ..
# r8  101  98  81 .. 18    1
# r9  100  99  80    19    0

def koordinaten_index(r,c):
    "Abbildung i -> r,c"
    top = (NROWS*NCOLS-1) - NROWS*c # Oberste Reihe
    return top-r if c % 2 == 0 else top-(NROWS-1)+r

def index_koordinaten(i):
    "Abbildung r,c -> i"
    c = NROWS-math.floor(i / NROWS)
    top = NROWS*NCOLS-1 - NROWS*c
    r = top-i if c%2 == 0 else i-top+NROWS-1
    return r,c

def index_range():
    return range(NROWS*NCOLS)

def koordinaten_range():
    return itertools.product( range(NROWS), range(NCOLS))

# Die im Satz zu nutzende Stunde
S = Enum('Stunde',[
    "DIESE",    # Rendere diese Stunde
    "NÄCHSTE",  # Rendere diese Stunde
    "VOLLE"     # Rendere diese Stunden zur vollen Stunde (EIN <-> EINS)
])

# Satzfragmente in Abhängigkeit von der Minute
# "ES IST"  und "UHR" fehlen und müssen immer dazu gesetzt werden
SATZ_INDEX = [
    [S.VOLLE, W.UHR], # Minute 0..5
    [W.FÜNF_A, W.NACH, S.DIESE], # Minute 5..10
    [W.ZEHN_A, W.NACH, S.DIESE], # ...
    [W.VIERTEL, W.NACH, S.DIESE],
    [W.ZWANZIG, W.NACH, S.DIESE],
    [W.FÜNF_A, W.VOR, W.HALB, S.NÄCHSTE],
    [W.HALB, S.NÄCHSTE],
    [W.FÜNF_A, W.NACH, W.HALB, S.NÄCHSTE],
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
    return [W.ES,W.IST] + SATZ_INDEX[satz_index(ti)]

# Stundenworte zur Stunde
STUNDEN = [W.ZWÖLF,W.EINS,W.ZWEI,W.DREI_B,W.VIER,W.FÜNF_B,W.SECHS,W.SIEBEN,W.ACHT,W.NEUN,W.ZEHN_B,W.ELF]

def stundenwort(st):
    "Stundenwort zur Stunde"
    return STUNDEN[st % len(STUNDEN)]

def ersetze_stunde(wort,ti):
    "Ersetze S.DIESE/S.NÄCHSTE/S.VOLLE durch Stundenwort"
    if wort == S.DIESE:
        return stundenwort(ti.hour)
    if wort == S.NÄCHSTE:
        return stundenwort(ti.hour+1)
    if wort == S.VOLLE:
        return W.EIN if ti.hour in (1,13) else stundenwort(ti.hour)
    return wort

def wort_indexe(w):
    "Tupel mit allen Indexen für ein Wort: (w,[i0,i1...])"
    return (w,[koordinaten_index(*k) for k in wort_koordinaten(w)])

def default_zeit():
    return datetime.datetime.now().time()

def zeit_satz(ti=None):
    "Vollständiger Satz zur Urzeit als Liste von Worten"
    t = ti if ti else default_zeit()
    return [ersetze_stunde(w,t) for w in satz_vorlage(t)]

def zeit_satz_indexe(ti=None):
    "Alle Indexe des Satzes zur Zeit ti"
    l = sum( (wort_indexe(i)[1] for i in zeit_satz(ti)), [] )
    l.sort()
    return l

def index_buchstaben_pos(il=None):
    "Liste mit (b,i,r,c) für Indexe"
    l = il if il else index_range()
    t = []
    for i in l:
        r,c = index_koordinaten(i)
        t.append((koordinaten_buchstabe(r,c),i,r,c))
    return t

def index_test_string(il=None):
    "Indexliste gerendert als String für die Terminal-Ausgabe"
    t = index_buchstaben_pos(il)
    return "\n".join( "".join(b for (b,i,r,c) in t if r==ar) for ar in range(NROWS) )

def zeit_ascii_string(ti=None):
    "Uhrzeit gerendert als String für die Terminal-Ausgabe"
    return index_test_string(zeit_satz_indexe(ti))

def zeit_spi_generator(ti=None):
    bg_color = SCHWARZ
    fg_color = ROT
    while True:
        t = ti if ti else default_zeit()
        s = zeit_satz_indexe(t)
        yield list( (fg_color if i in s else bg_color) for i in index_range() )
#
# Test starten:
#     python3 -m unittest c3.hclock
#
class HTest(unittest.TestCase):
    def testSatzIndex(self):
        self.assertEqual(zeit_satz_indexe(time(11,5,0)),
            [6, 9, 10, 13, 26, 29, 30, 33, 34, 45, 50, 54, 69, 70, 90, 109])
    def testWort(self):
        self.assertEqual(W.ACHT.name,"ACHT")
        self.assertEqual(wort_stamm(W.ACHT),"ACHT")
        self.assertEqual(wort_stamm(W.ZEHN_A),"ZEHN")
        self.assertEqual(wort_stamm(W.ZWÖLF),"ZWÖLF")
        self.assertEqual(wort_stamm(W.FÜNF_A),"FÜNF")
    def testKoordinaten(self):
        self.assertEqual(wort_koordinaten(W.ES),[(0,0),(0,1)])
        self.assertEqual(wort_koordinaten(W.EIN),[(5,0),(5,1),(5,2)])
        self.assertEqual(wort_koordinaten(W.EINS),[(5,0),(5,1),(5,2),(5,3)])
        self.assertEqual(wort_koordinaten(W.FÜNF_A),[(0,7),(0,8),(0,9),(0,10)])
        self.assertEqual(wort_koordinaten(W.ACHT),[(7,7),(7,8),(7,9),(7,10)])
        self.assertEqual(len(list(koordinaten_range())),110)
        self.assertEqual(len(set(koordinaten_range())),110)
        self.assertEqual(min(koordinaten_range()),(0,0))
        self.assertEqual(max(koordinaten_range()),(NROWS-1,NCOLS-1))
        self.assertEqual(koordinaten_buchstabe(0,0),'E')
        self.assertEqual(koordinaten_buchstabe(9,10),'R')
    def testKoordinatenIndex(self):
        self.assertEqual(len(index_range()),NROWS*NCOLS)
        self.assertEqual(len(set(index_range())),NROWS*NCOLS)
        self.assertEqual(min(index_range()),0)
        self.assertEqual(max(index_range()),NROWS*NCOLS-1)
        self.assertEqual(koordinaten_index(0,0),109)
        self.assertEqual(koordinaten_index(9,0),100)
        self.assertEqual(koordinaten_index(0,1),90)
        self.assertEqual(koordinaten_index(9,1),99)
        self.assertEqual(koordinaten_index(0,10),9)
        self.assertEqual(koordinaten_index(9,10),0)
        self.assertEqual(index_koordinaten(100),(9,0))
        for i in index_range():
            self.assertEqual(koordinaten_index(*index_koordinaten(i)),i)
    def testWortIndexe(self):
        self.assertEqual(wort_indexe(W.ES), (W.ES,[109,90]))
        self.assertEqual(wort_indexe(W.UHR), (W.UHR,[20,19,0]))
        self.assertEqual(wort_indexe(W.FÜNF_A), (W.FÜNF_A,[30,29,10,9]))
        self.assertEqual(wort_indexe(W.ZEHN_B), (W.ZEHN_B,[100,99,80,79]))
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
        self.assertEqual(zeit_satz(time(1,5,0)),[W.ES,W.IST,W.FÜNF_A,W.NACH,W.EINS])
        self.assertEqual(zeit_satz(time(1,25,0)),[W.ES,W.IST,W.FÜNF_A,W.VOR,W.HALB,W.ZWEI])
        self.assertEqual(zeit_satz(time(12,55,0)),[W.ES,W.IST,W.FÜNF_A,W.VOR,W.EINS])
        self.assertEqual(zeit_satz(time(13,5,0)),[W.ES,W.IST,W.FÜNF_A,W.NACH,W.EINS])
        self.assertEqual(zeit_satz(time(11,4,59)),[W.ES,W.IST,W.ELF,W.UHR])
        self.assertEqual(zeit_satz(time(11,5,0)),[W.ES,W.IST,W.FÜNF_A,W.NACH,W.ELF])
        self.assertEqual(zeit_satz(time(11,10)),[W.ES,W.IST,W.ZEHN_A,W.NACH,W.ELF])
        self.assertEqual(zeit_satz(time(11,15)),[W.ES,W.IST,W.VIERTEL,W.NACH,W.ELF])
        self.assertEqual(zeit_satz(time(11,54,59)),[W.ES,W.IST,W.ZEHN_A,W.VOR,W.ZWÖLF])
        self.assertEqual(zeit_satz(time(11,55)),[W.ES,W.IST,W.FÜNF_A,W.VOR,W.ZWÖLF])
        self.assertEqual(zeit_satz(time(11,59,59)),[W.ES,W.IST,W.FÜNF_A,W.VOR,W.ZWÖLF])
        self.assertEqual(zeit_satz(time(1,0)),[W.ES,W.IST,W.EIN,W.UHR])
        self.assertEqual(zeit_satz(time(13,0)),[W.ES,W.IST,W.EIN,W.UHR])
        self.assertEqual(zeit_satz(time(23,0)),[W.ES,W.IST,W.ELF,W.UHR])
