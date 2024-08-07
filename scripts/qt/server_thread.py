import sys
import socket

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

    def run(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        client, address = server.accept()
        self.client_connected.emit()

        while True:
            message = client.recv(1024).decode("utf-8")
            print("loop")
            if message == "/close":
                print("close operation begun")
                client.close()
                server.close()
                self.connection_closed.emit()
                break
            elif message == "/clear":
                print("clearing inbox")
                self.message_clear.emit()
            else:
                print(message)
                self.message_received.emit(message)
                print("continue operation")

        client.close()
        server.close()

