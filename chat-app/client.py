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

def signal_handler(sig, frame):
    os._exit(1)

def home_screen(stdscr):

    while True:

        key = stdscr.getch()
        if key != -1:
            return

        stdscr.clear()
        stdscr.addstr(art.HOME_SCREEN)
        stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.wrapper(home_screen)


if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, signal_handler)

    curses.wrapper(main)