from copy import copy
import getpass
import signal
import socket
import os
import threading
import time
import sys

from cryptography.fernet import Fernet

from getch import get_input

HOME = f"/Users/{getpass.getuser()}"


def thread(func):
    """Exception handling decorator for threads"""
    def thread_with_exception_handling(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            if str(e) == 'keyboard interrupt':
                print('exiting the server...')
            else:
                error_file = f'{HOME}/chat-app-errors'
                with open(error_file, 'w+') as f:
                    f.write(str(e))
                print(f'Program failed. See {error_file} for traceback.')
            os._exit(1)
    return thread_with_exception_handling


def signal_handler(sig, frame):
    print("exiting the server...")
    os._exit(1)


@thread
def send_messages(username):
    """
    Sends input to server which
    sends to other clients
    """

    def sense_change(chars):
        """
        Sends signals to server when user is typing or has stopped typing
        
        {username} >> 5 means user has started typing
        {username} >> 6 means user has stopped typing
        """
        previous_chars = chars[:]
        frame = 0
        # the most recent frame where there was a difference between previous_chars and chars
        last_frame_typing = 0
        current_state = "lazy"
        while True:
            if previous_chars != chars:
                if current_state == "lazy":
                    s.send(f'{username} >> 6')
                    current_state = "typing"
                previous_chars = chars[:]
                last_frame_typing = copy(frame)
            else:
                if (current_state == "typing") and (frame - last_frame_typing == 200):
                    s.send(f'{username} >> 5')
                    current_state = "lazy"
                    
            frame += 1
            time.sleep(0.01)

    @thread
    def get_message_inputs():
        while True:
            chars = []
            get_input(chars)
            msg = ''.join(chars)
            if msg != "":
                s.send(bytes(msg, "utf-8"))
            print("\033[A                             \033[A")

    gi = threading.Thread(target=get_message_inputs)
    gi.start()


@thread
def receive_messages(username):
    """
    Constantly reveieves data from
    server and prints to console
    """
    while True:
        data = s.recv(1024).decode("utf-8")
        if data[0] == "1":
            user = data[1:].split(": ")[0] + ": "
            message = data[1:][len(user):]
            if user[:-2] != username:
                print(f"\033[1;34m{user}\033[0m{message}")
            else:  # message was sent by user
                print(f"\033[1;32m{user}\033[0m{message}")
        elif data[0] == "2":
            if "joined the server" in data:
                print(f"\033[32m{data[1:]}\033[0m")
            else:
                print(f"\033[31m{data[1:]}\033[0m")
        sys.stdout.write('\r')
        sys.stdout.flush()


if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, signal_handler)
    
    os.system("stty -echo") 
    password = input("Password: ")
    os.system("stty echo")
    print() 

    with open(f"{HOME}/.chat-app.key", "rb") as f:
        key = f.read()
    
    fernet = Fernet(key)
    
    # read encrypted message
    with open(f'{HOME}/.chat-app-user-secrets', 'rb') as f:
        encrypted = f.read()

    if password == fernet.decrypt(encrypted).decode("utf-8"):
    
        server = input("server: ")
        port = input("port: ")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, int(port)))
        print("\033[1;32mSuccessfully connected to the server!\033[0m")   
        
        username = input("username: ")
        s.send(bytes(username, 'utf-8'))    

        sm = threading.Thread(target=send_messages, args=[username])
        rm = threading.Thread(target=receive_messages, args=[username])
        sm.start()
        rm.start()
    else:
        print('incorrect password')
