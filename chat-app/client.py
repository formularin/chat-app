from copy import copy
import getpass
import signal
import socket
import os
import threading
import time
import traceback
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
                    f.write(traceback.format_exc())
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

    @thread
    def sense_change(chars, enter_pressed):
        """
        Sends signals to server when user is typing or has stopped typing
        
        5 means user has started typing
        6 means user has stopped typing
        """
        previous_enter_pressed = 0
        previous_chars = chars[:]
        frame = 0
        # the most recent frame where there was a difference between previous_chars and chars
        last_frame_typing = 0
        current_state = "lazy"

        while True:

            if previous_enter_pressed != enter_pressed.value:
                last_frame_typing = 0
                frame = 0
                current_state = "lazy"
                previous_enter_pressed = copy(enter_pressed.value)

            if previous_chars != chars:
                if current_state == "lazy":
                    # started typing
                    s.send(bytes('5', 'utf-8'))
                    current_state = "typing"
                previous_chars = chars[:]
                last_frame_typing = copy(frame)
            else:
                if (current_state == "typing") and (frame - last_frame_typing == 200):
                    # stoppped typing
                    s.send(bytes('6', 'utf-8'))
                    current_state = "lazy"

            frame += 1
            time.sleep(0.01)

    @thread
    def get_message_inputs(chars, enter_pressed):
        while True:
            get_input(chars)
            enter_pressed.increment()
            msg = ''.join(chars)
            if msg != "":
                s.send(bytes(msg, "utf-8"))
            print("\033[A                             \033[A")
            for i in range(len(chars)):
                chars.pop(0)

    class EnterPressed:
        """dummy class that can be changed from within function"""
        def __init__(self):
            self.value = 0
        def increment(self):
            self.value += 1

    enter_pressed = EnterPressed()
    chars = []
    gi = threading.Thread(target=get_message_inputs, args=(chars, enter_pressed,))
    sc = threading.Thread(target=sense_change, args=(chars, enter_pressed,))
   
    gi.start()
    sc.start()


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
        elif data[0] == "4":
            print(data[1:])
        sys.stdout.write('\r')
        sys.stdout.flush()


if __name__ == "__main__":
    
    signal.signal(signal.SIGINT, signal_handler)
    
    argv = sys.argv[1:]
    if len(argv) < 2:
        raise Exception('requires server ip and port number as arguments')

    server = argv[0]
    port = argv[1]

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
