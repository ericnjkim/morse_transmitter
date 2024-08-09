import sys
import socket
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from scripts.core.functions_socket.functions_server import create_local_ip, start_server


# try adding client handler into this qthread

""" Usually I'd prefer to have logic in the core directory but in this case I 
needed to wire the loop that received messages with a signal emitter.
"""

class ServerThread(QThread):
    """ Operations for the transmitter's ability to connect to another
    transmitter and for handling received messages.
    """
    # client_connected = pyqtSignal(tuple)
    client_connected = pyqtSignal()
    message_received = pyqtSignal(str)
    message_clear = pyqtSignal()
    connection_closed = pyqtSignal()

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

        self.connection_map = {} # socket, addr
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        # self.client_connected.emit()

        while True:
            connection_socket, address = self.server_socket.accept()
            if len(self.connection_map) == 2:
                connection_socket.sendall(f"This connection is occupied.".encode("utf-8"))
                continue

            print(f"Connected: {address}")
            connection_id = len(self.connection_map) + 1
            self.connection_map[connection_id] = {"socket": connection_socket, "address": address}

            self.broadcast(f"/server_status connection:{address}")
            connection_socket.send("SERVER: successful connection".encode("utf-8"))

            server_socket = ServerSocketThread(connection_socket, connection_id, self)
            server_socket.start()

    def remove_connection(self, id):
        self.connection_map[id]["socket"].close()
        self.connection_map.pop(id)

            # message = client.recv(1024).decode("utf-8")
            # print("loop")
            # if message == "/close":
            #     print("close operation begun")
            #     client.close()
            #     server.close()
            #     self.connection_closed.emit()
            #     break
            # elif message == "/clear":
            #     print("clearing inbox")
            #     self.message_clear.emit()
            # else:
            #     print(message)
            #     self.message_received.emit(message)
            #     print("continue operation")


    def broadcast(self, message, sender_id=None):
        for id in self.connection_map:
            if id != sender_id:
                self.connection_map[id]["socket"].send(message.encode("utf-8"))

    def close_server(self):
        for id in self.connection_map:
            self.connection_map[id]["socket"].close()
        print("Server shutting down...")
        os._exit(0)

class ServerSocketThread(QThread):

    def __init__(self, socket_connection, id, server):
        super().__init__()
        self.socket_connection = socket_connection
        self.id = id
        self.server = server

    def run(self):
        while True:
            message = self.socket_connection.recv(1024).decode("utf-8")

            if message:
                # print(f"{self.socket_name}: {message}")
                self.server.broadcast(message, self.id)
            else:
                # print(f"{self.id} has closed connection.")
                self.socket_connection.close()
                self.server.remove_connection(self.id)
                break
