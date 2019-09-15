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
    n_messages = 0
    username = ""
    while True:
        msg = clientsocket.recv(1024)
        if msg != b'':
            if n_messages == 0:
                username = msg.decode("utf-8")
                msg = username + " has joined the server!"
                for c in clientsockets[:-1]:
                    c.send(bytes(msg, "utf-8"))
            else:
                msg = f"{username}: " + msg.decode("utf-8")
                for c in clientsockets:
                    c.send(bytes(msg, "utf-8"))

            n_messages += 1
        else:
            clientsocket.close()
            clientsockets.remove(clientsocket)
            addresses.remove(address)
            print(f"Connection for {address} has been severed")
            for c in clientsockets:
                c.send(bytes(username + " has left the server", "utf-8"))
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
