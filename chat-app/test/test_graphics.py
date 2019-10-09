"""Currently the mainloop for an input and retreive data system"""


import curses
import sys
from os.path import abspath, dirname
import time

cwd = '/'.join(abspath(dirname(__file__)).split('/')[:-1])
sys.path.append(cwd)

import graphics

def main(stdscr):

    canvas = graphics.Canvas(curses.LINES, curses.COLS - 1)
    input_line = graphics.InputLine(canvas, "password: ")

    stdscr.nodelay(True)
    while True:
        
        key = stdscr.getch()

        if input_line.submitted == False:
            input_line.type_char(key)
            input_line.render()
        else:
            break

        stdscr.clear()
        stdscr.addstr(canvas.display)
        stdscr.refresh()

        time.sleep(0.01)

    while True:

        stdscr.clear()
        stdscr.addstr(f"your password is: {input_line.value}")
        stdscr.refresh()

        time.sleep(0.01)


if __name__ == "__main__":
    curses.wrapper(main)
    # canvas = graphics.Canvas(5, 20)
    # input_line = graphics.InputLine(canvas, "password: ")

    # input_line.add_char("a")
    # input_line.render()
    # print(canvas.display)