import time
import sys

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


def get_input(chars):
    """
    Gets keyboard input and constantly
    edits list `chars` accordingly
    """
    with open('/Users/Mukeshkhare/Desktop/projects/python/chat-app/file.txt', 'w') as f:
        getch = _Getch()
        while True:
            key = getch()
            if ord(key) == 3:
                raise KeyboardInterrupt
            elif ord(key) == 127:
                try:
                    chars.pop(-1)
                    sys.stdout.write('\b')
                    sys.stdout.write(' ')
                    sys.stdout.write('\b')
                    sys.stdout.flush()
                except IndexError:
                    pass
            elif ord(key) == 13:
                sys.stdout.write('\n')
                sys.stdout.flush()
                return
            else:
                chars.append(key)
                sys.stdout.write(key)
                sys.stdout.flush()
            f.write(''.join(chars))
            time.sleep(0.01)