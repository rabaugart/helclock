import curses, time

from .hclock import index_buchstaben_pos, zeit_satz_indexe

class CRenderer:
    def run(self):
        count = True
        w = curses.initscr()
        w.timeout(100)
        curses.savetty()
        w.clear()
        w.border()
        cw = 13
        while count:
            ch = w.getch()
            if ch >= 0:
                cw = ch
            w.clear()
            w.addstr(1,1,"Beenden mit q")
            for b,i,r,c in index_buchstaben_pos(zeit_satz_indexe()):
                w.addstr( 5+2*r, 5+3*c, b)
            w.refresh()
            if ch == 113:
                count = False
        curses.resetty()

CR = CRenderer()
