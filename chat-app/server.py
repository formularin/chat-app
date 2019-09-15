import socket
import signal
import sys
import threading

# ^c catching
def signal_handler(sig, frame):
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1237))
s.listen(5)

clientsockets = []
addresses = []

def handle_client_message(clientsocket, address):
    """
    Send recieved message back to 
    client and also print to console
    """
    while True:
        msg = clientsocket.recv(1024)
        if msg != b'':
            msg = f"{address}: " + msg.decode("utf-8")

            with open('/Users/Mukeshkhare/Desktop/thing.txt', 'w+') as f:
                f.write(msg)

            for c in clientsockets:
                c.send(bytes(msg, "utf-8"))

            print(msg)

while True:
    
    # make connection
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    clientsockets.append(clientsocket)
    addresses.append(address)


    # create thread to constantly be looking for new connections, but still respond to messages
    x = threading.Thread(target=handle_client_message, args=(clientsocket, address))
    x.start()

