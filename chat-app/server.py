import socket
import sys
import threading

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 1237))
s.listen(5)

# client info
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

            for c in clientsockets:
                c.send(bytes(msg, "utf-8"))
        else:
            clientsocket.close()
            clientsockets.remove(clientsocket)
            addresses.remove(address)
            break

def create_connections():
    """
    Constantly look for clients to connect with
    """
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established!")
        clientsockets.append(clientsocket)
        addresses.append(address)
        hcm = threading.Thread(target=handle_client_message, args=(clientsocket, address))
        hcm.start()

if __name__ == "__main__":
    create_connections()
