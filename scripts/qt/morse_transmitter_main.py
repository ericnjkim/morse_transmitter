import os
import sys
import threading
from datetime import datetime


from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog

from scripts.core.functions_morse_translator import translate
from scripts.core.functions_socket.functions_client import start_client
from scripts.core.functions_socket.functions_server import start_server, create_local_ip, handle_client
from scripts.qt.server_thread import ServerThread
from scripts.qt.client_handler_thread import ClientHandlerThread

UI_FILE = f"{os.path.dirname(__file__)}/ui/morse_transmitter_main.ui"

# - Connect buttons to keyboard buttons as well.
# - See if I can get the morse buttons to be replaced with a single button and
# work off timing for dots and dashes.
# # add keyboard inputs

# close off pte to manual typing
# add receiving message box

# if someone connects to this server, immediately connect to them too

class MorseTransmitter(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        self.btn_dot.clicked.connect(self._btn_dot)
        self.btn_dash.clicked.connect(self._btn_dash)
        self.btn_slash.clicked.connect(self._btn_slash)
        self.btn_clear.clicked.connect(self._btn_clear)

        self.btn_start_host.clicked.connect(self._btn_start_host)
        self.btn_connect.clicked.connect(self._btn_connect)

        self.current_letter = ""
        self.space_detector = 0

        local_ip = create_local_ip()
        self.ledit_local_ip.setText(local_ip)
        self.server_thread = ServerThread(local_ip, 5050)
        self.server_thread.client_connected.connect(self._handle_client)
        self.client_handler_thread = ClientHandlerThread(None, "", "")
        self.client_handler_thread.message_received.connect(self._print_received_message)

    def _btn_start_host(self):
        # server seems to be stopping all other operations from running so it
        # needs to be on its own thread
        self.server_thread.start()
        self.ledit_connection_status.setText("server started...")
        # thread_start_server = threading.Thread(target=start_server(local_ip))
        # thread_start_server.start()
        # start_server(local_ip)

    def _handle_client(self, connection_data):
        client, port, server = connection_data
        print('run client handle', connection_data)
        self.client_handler_thread.client = client
        self.client_handler_thread.port = port
        self.client_handler_thread.server = server
        self.client_handler_thread.start()

    def _print_received_message(self, message):
        # add clear event
        # add close event
        print(message)
        self.pte_message_recv.insertPlainText(message)

    def _btn_dot(self):
        self.current_letter += "."

    def _btn_dash(self):
        self.current_letter += "_"

    def _btn_slash(self):
        """ Slash is used to signify the end of a letter and two signify a
        space.
        """
        self.space_detector += 1
        if self.space_detector == 2:
            self.pte_message_sent.insertPlainText(" ")
            self.space_detector = 0
            return None

        character = translate(self.current_letter)
        if character:
            self.pte_message_sent.insertPlainText(character)
            self.current_letter = ""
            self.space_detector = 0

    def _btn_clear(self):
        """ Clears the sent message text window."""
        self.pte_message_sent.clear()
        self.space_detector = 0

    def _btn_connect(self):
        """ Initiates the connection between the local transmitter and a target
        transmitter.
        """
        receiver_ip = self.ledit_receiver_ip.text()
        # have some sort of check if the ip was valid or not.
        start_client(receiver_ip)

# plaint text edit needs to be uneditable
if __name__ == "__main__":
    from pathlib import Path

    app = QApplication(sys.argv)
    # app.setStyleSheet(Path('material_dark.qss').read_text())
    window = MorseTransmitter()
    window.show()
    sys.exit(app.exec_())

    # btn = QtWidgets.QPushButton()
    # [print(i) for i in dir(btn)]