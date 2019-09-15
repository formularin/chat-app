import socket
import signal
import sys

# ^c catching
def signal_handler(sig, frame):
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1235))
s.listen(5)

while True:
    
    # make connection
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    
    # send messages
    while True:
        msg = clientsocket.recv(1024)
        clientsocket.send(msg)
        print(f"{address}:", msg.decode("utf-8"))
