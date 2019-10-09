import curses
import getpass
import signal
import socket
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


def main(stdscr):
    
    try:
        stdscr.nodelay(True)
        curses.curs_set(0)
        home_screen(stdscr)

        canvas = graphics.Canvas(curses.LINES, curses.COLS - 1)
        password_input = graphics.InputLine(canvas, "password: ", echo=False)
        cursor = graphics.Cursor(canvas)

        frame = 0
        while True:
            
            key = stdscr.getch()

            if password_input.submitted == False:
                
                # update conceptual renderings of images
                password_input.type_char(key)
                cursor.move(0, password_input.cursor_index)
                if frame % 10 == 0:
                    cursor.toggle_char()
                
                # display image changes on canvas
                password_input.render()
                cursor.render()


                with open('/Users/Mukeshkhare/Desktop/projects/python/chat-app/file.txt', 'w') as f:
                    f.write(password_input.value)

            else:
                break
                
            # display canvas on screen
            stdscr.clear()
            stdscr.addstr(canvas.display)
            stdscr.refresh()

            frame += 1
            time.sleep(0.01)

        password = password_input.value

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

    except ExitException:
        return  # exit function


if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, signal_handler)

    curses.wrapper(main)