import socket
import threading


# starting server
# if server is already active use that one, else start server

PORT = 5051
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
DISCONNECT_MSG = "disconnected"

# DISCONNECT_MSG = "disconnected"