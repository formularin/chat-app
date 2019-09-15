import curses

def main(stdscr):
    while True:
        key = stdscr.getch()
        stdscr.clear()
        stdscr.addstr(str(key))
        stdscr.refresh()

curses.wrapper(main)
