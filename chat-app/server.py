import curses
import getpass
import os
import signal
import socket
import subprocess
import sys
import threading

from cryptography.fernet import Fernet


def signal_handler(sig, frame):
    os._exit(1)


def main():
    pass


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    curses.wrapper(main)
