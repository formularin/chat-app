import curses
import socket
import string
import threading


class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[" " for _ in range(self.width)] for _ in range(self.height())]
    @property

    def display(self):
        return "\n".join(["".join(row) for row in self.grid])

    def replace(self, x, y, char):
        self.grid[y][x] = char


class Message:  
    def __init__(self, x, y, text, canvas):
        self.x = x
        self.y = y
        self.text = text
        self.canvas = canvas
    
    def render(self):
        for char in self.text:
            self.canvas.replace(
                self.x,
                self.y + self.text.index(char),
                char
            )


server = input()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, 1237))

def send_messages(stdscr, canvas):
    """
    Sends input to server which
    sends to other clients
    """
    while True:
        # TODO: input for msg
        key = stdscr.getch()  # for now you can only send one char at a time
        if chr(key) in string.printable:
            s.send(bytes(chr(key), "utf-8"))

def receive_messages(stdscr, canvas):
    """
    Constantly receives data from
    server and prints to console
    """
    n_messages = 0
    while True:
        data = s.recv(1024)
        msg = Message(x)
        stdscr.addstr(data.decode("utf-8"))

def main(stdscr):
    c = Canvas(curses.COLS - 1, curses.LINES - 2)
    
    sm = threading.Thread(target=send_messages, args=[stdscr, c])
    rm = threading.Thread(target=receive_messages, args=[stdscr, c])
    sm.start()
    rm.start()

if __name__ == "__main__":
    curses.wrapper(main)
