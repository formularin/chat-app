import socket

server = input()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, 1235))

while True:
    msg = s.recv(1024)
    print(msg.decode("utf-8"))


