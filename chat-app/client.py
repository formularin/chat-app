import socket
import threading

server = input()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, 1237))

def send_messages():
    """
    Sends input to server which
    sends to other clients
    """
    while True:
        msg = input()
        s.send(bytes(msg, "utf-8"))

def receive_messages():
    """
    Constantly receives data from
    server and prints to console
    """
    while True:
        data = s.recv(1024)
        print(data.decode("utf-8"))

sm = threading.Thread(target=send_messages)
rm = threading.Thread(target=receive_messages)
sm.start()
rm.start()
