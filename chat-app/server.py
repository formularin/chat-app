import socket
import signal
import sys

def signal_handler(sig, frame):
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("localhost", 1235))
    s.listen()

    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    while True:
        msg = input()
        clientsocket.send(bytes(msg, "utf-8"))
