import curses
import getpass
import signal
import socket
import sys
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
    """Displays home screen"""

    # stdscr.nodelay(True) has already been called

    while True:

        key = stdscr.getch()
        if key != -1:  # if key isn't nothing
            return

        stdscr.clear()
        stdscr.addstr(art.HOME_SCREEN)
        stdscr.refresh()

        time.sleep(0.01)


def ask_for_input(stdscr, cursor, canvas, prompt, echo=True):
    """Creates input line at bottom of screen"""

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
    
    return input_line.value  # return submitted text


def send_messages(stdscr, cursor, canvas, s):
    """
    Sends input to server which
    sends to other clients
    """
    while True:
        msg = ask_for_input(stdscr, cursor, canvas, "message: ")
        if msg != "":
            s.send(bytes(msg, "utf-8"))


def main(stdscr, server, port):
    
    try:
        stdscr.nodelay(True)  # don't wait for keypress
        curses.curs_set(0)  # hide cursor
        
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
            # if correct
            pass
        else:
            # if incorrect
            while True:
                stdscr.clear()
                stdscr.addstr("incorrect password, press ^c to quit")
                # typing ^c will lead to except block and exit function
                stdscr.refresh()
                time.sleep(0.01)

        # connect to server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, int(port)))

        # connect to server
        username = ask_for_input(stdscr, cursor, canvas, "username: ")
        s.send(bytes(username, 'utf-8'))

        send_messages(stdscr, cursor, canvas, s)

    except ExitException:
        return


if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, signal_handler)  # handle ^c

    # server ip and port are command-line args
    try:
        server, port = sys.argv[1:3]
    except ValueError:
        raise Exception("no inputted server or port.")

    curses.wrapper(main, server, port)