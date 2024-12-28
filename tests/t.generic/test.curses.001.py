import curses

def main(stdscr):
    curses.curs_set(0)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    print("\033[?1003h\n") # allows capturing mouse movement

    while True:
        c = stdscr.getch()
        if c == curses.KEY_MOUSE:
            try:
                event = curses.getmouse()
                x = event[2]
                y = event[1]
                dims = stdscr.getmaxyx()
                stdscr.addstr(0,0,"="*dims[1])
                stdscr.addstr(0,dims[1]-len(str(dims)),str(dims))
                stdscr.addstr(0,0,str(event))
                if event[4] == 4:
                    stdscr.addstr(x,y,"X")
                else:
                    stdscr.addstr(x,y,"*")
            except:
                pass
        stdscr.refresh()

curses.wrapper(main)