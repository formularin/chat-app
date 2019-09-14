import socket
import signal
import sys

def signal_handler(sig, frame):
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1235))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    while True:
        msg = input()
        clientsocket.send(bytes(msg, "utf-8"))
