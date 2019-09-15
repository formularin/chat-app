import curses
import socket

server = input()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, 1235))

while True:
    msg = input()
    s.send(bytes(msg, "utf-8"))
    data = s.recv(1024)
    print("client:", data.decode("utf-8"))
