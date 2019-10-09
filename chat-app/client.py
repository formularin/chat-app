import curses
import getpass
import signal
import socket
import os
import threading
import time

from cryptography.fernet import Fernet

import graphics
import art

class ExitException(Exception):
    """Dummy exception for exiting script on ^c"""

def signal_handler(sig, frame):
    raise ExitException()

def home_screen(stdscr):

    while True:

        key = stdscr.getch()
        if key != -1:
            return

        stdscr.clear()
        stdscr.addstr(art.HOME_SCREEN)
        stdscr.refresh()

        time.sleep(0.01)


def main(stdscr):
    
    try:
        stdscr.nodelay(True)
        curses.curs_set(0)
        home_screen(stdscr)

        canvas = graphics.Canvas(curses.LINES, curses.COLS - 1)
        password_input = graphics.InputLine(canvas, "password: ")

        while True:
            
            key = stdscr.getch()

            if password_input.submitted == False:
                password_input.type_char(key)
                password_input.render()
            else:
                break

            stdscr.clear()
            stdscr.addstr(canvas.display)
            stdscr.refresh()

            time.sleep(0.01)

        password = password_input.value

    except ExitException:
        return  # exit function


if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, signal_handler)

    curses.wrapper(main)