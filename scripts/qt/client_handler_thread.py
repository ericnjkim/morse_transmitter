"""since we can't just have a return function in a loop
, we need to emit the data each time there is new data
to make sure we can have a constant stream of data.
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from scripts.core.functions_socket.functions_server import handle_client

class ClientHandlerThread(QThread):
    message_received = pyqtSignal(str)
    connection_closed = pyqtSignal(int)

    def __init__(self, client, address, server):
        super().__init__()
        self.client = client
        self.address = address
        self.server = server

    def run(self):

        while True:
            message = self.client.recv(1024).decode("utf-8")
            if message == "/close":
                break
            else:
                print(message)
                self.message_received.emit(message)

            self.client.send(input("Message: ").encode("utf-8"))

        self.client.close()
        self.server.close()
        self.connection_closed.emit(1)
