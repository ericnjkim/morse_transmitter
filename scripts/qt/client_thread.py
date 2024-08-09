import sys
import socket
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

# try adding client handler into this qthread

class ClientThread(QThread):

    message_received = pyqtSignal(str)
    message_clear = pyqtSignal()

    def __init__(self, server_host, server_port, id):
        super().__init__()
        self.server_host = server_host
        self.server_port = server_port
        self.id = id
        self.message_to_send = ""

        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.receive_thread = ClientReceiveThread(self)
        self.receive_thread.received_message.connect(self.handle_received_message)

    # def update_message_to_send(self, message):
    #     self.message_to_send = message


    def run(self):
        self.connection_socket.connect((self.server_host, self.server_port))
        self.receive_thread.start()

    def send_message(self, message):
        if message == "/quit":
            self.connection_socket.send("Recipient disconnected".encode("utf-8"))
            self.connection_socket.close()
            print("Could not send. Disconnecting...")

        self.connection_socket.send(message.encode("utf-8"))

    def handle_received_message(self, message):
        # apply message onto pte


class ClientReceiveThread(QThread):

    received_message = pyqtSignal(str)

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while True:
            try:
                message = self.client.connection_socket.recv(1024).decode("utf-8")
                if message:
                    self.received_message.emit(message)
            except:
                self.client.connection_socket.close()
                break

class ClientSendThread(QThread):
    # made as its own class but it can probably exist outside of a class

    def __init__(self, client):
        super().__init__()
        self.client = client

    def send_message(self, message):

        if message == "/quit":
            self.client.connection_socket.send("Recipient disconnected".encode("utf-8"))
            self.client.connection_socket.close()
            print("Could not send. Disconnecting...")

        self.client.connection_socket.send(message.encode("utf-8"))