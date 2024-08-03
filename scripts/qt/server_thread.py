import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from scripts.core.functions_socket.functions_server import create_local_ip, start_server


class ServerThread(QThread):
    client_connected = pyqtSignal(tuple)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        client, address, server = start_server(self.host, self.port)
        print(client, "client found")
        self.client_connected.emit((client, address, server))