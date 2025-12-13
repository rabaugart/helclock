import curses, time

class CRenderer:
    def run(self):
        w = curses.initscr()
        curses.savetty()
        w.clear()
        w.border()
        w.addstr(5,7,f'X {curses.COLS}')
        w.addstr(9,7,f'Y {curses.LINES}')
        w.refresh()
        time.sleep(2)
        curses.resetty()

CR = CRenderer()
