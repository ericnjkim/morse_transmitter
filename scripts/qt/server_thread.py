import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal

from scripts.core.functions_socket.functions_server import create_local_ip, start_server


class ServerThread(QThread):
    output_started = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        self.transcriber_model_type = transcriber_model_type

    def run(self):
        client, address, server = start_server()
        han
        self.output_started.emit(transcribed_text)