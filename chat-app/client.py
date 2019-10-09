import curses
import getpass
import signal
import socket
import sys
import threading
import time

from cryptography.fernet import Fernet

import graphics
import art


HOME = f"/Users/{getpass.getuser()}"


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


def ask_for_input(stdscr, cursor, canvas, prompt, echo=True):

    input_line = graphics.InputLine(canvas, prompt, echo)
    
    frame = 0
    while True:

        key = stdscr.getch()

        if not input_line.submitted:

            # update conceptual renderings of images
            input_line.type_char(key)
            cursor.move(0, input_line.cursor_index)
            if frame % 10 == 0:
                cursor.toggle_char()
                
            # display image changes on canvas
            input_line.render()
            cursor.render()

        else:
            break

        # display canvas on screen
        stdscr.clear()
        stdscr.addstr(canvas.display)
        stdscr.refresh()

        frame += 1
        time.sleep(0.01)
    
    return input_line.value

def main(stdscr, server, port):
    
    try:
        stdscr.nodelay(True)
        curses.curs_set(0)
        home_screen(stdscr)

        canvas = graphics.Canvas(curses.LINES, curses.COLS - 1)
        cursor = graphics.Cursor(canvas)

        password = ask_for_input(stdscr, cursor, canvas, "password: ", False)

        # check if password is correct

        with open(f"{HOME}/.chat-app.key", "rb") as f:
            key = f.read()
    
        fernet = Fernet(key)
        
        # read encrypted message
        with open(f'{HOME}/.chat-app-user-secrets', 'rb') as f:
            encrypted = f.read()

        if password == fernet.decrypt(encrypted).decode("utf-8"):
            pass
        else:
            while True:

                stdscr.clear()
                stdscr.addstr("incorrect password, press ^c to quit")
                stdscr.refresh()
                time.sleep(0.01)

            return

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, int(port)))


    except ExitException:
        return  # exit function


if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, signal_handler)

    try:
        server, port = sys.argv[1:3]
    except ValueError:
        raise Exception("no inputted server or port.")

    curses.wrapper(main, server, port)