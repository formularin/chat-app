import curses
import socket


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
s.connect((server, 1235))

while True:
    msg = input()
    s.send(bytes(msg, "utf-8"))
    data = s.recv(1024)
    print("client:", data.decode("utf-8"))
