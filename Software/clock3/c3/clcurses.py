import curses, time

from .hclock import index_buchstaben_pos, zeit_satz_indexe

class CRenderer:
    TIMEOUT = 100 # ms
    UPDATE_ZYKLEN = 50
    def run(self):
        count = True
        w = curses.initscr()
        curses.savetty()
        curses.def_shell_mode()
        w.timeout(self.TIMEOUT)
        w.clear()
        w.border()
        cw = 13
        zyklus = 0
        while count:
            ch = w.getch()
            if ch == 113:
                count = False
            if ch >= 0:
                cw = ch
            zyklus = (zyklus+1) % self.UPDATE_ZYKLEN
            if zyklus != 1:
                continue
            w.clear()
            w.addstr(1,1,"Beenden mit q")
            for b,i,r,c in index_buchstaben_pos(zeit_satz_indexe(None,True)):
                w.addstr( 5+2*r, 5+3*c, b)
            w.refresh()
        curses.reset_shell_mode()
        curses.resetty()

CR = CRenderer()
