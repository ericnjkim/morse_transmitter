import os
import sys
import threading
import time
from datetime import datetime


from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog

from scripts.core.functions_morse_translator import translate
from scripts.core.functions_transmission_timer import MorseTransmissionTimer
from scripts.core.functions_socket.functions_client import start_client
from scripts.core.functions_socket.functions_server import start_server, create_local_ip, handle_client
from scripts.qt.server_thread import ServerThread

UI_FILE = f"{os.path.dirname(__file__)}/ui/morse_transmitter_main.ui"

# - See if I can get the morse buttons to be replaced with a single button and
# work off timing for dots and dashes.
# if someone connects to this server, immediately connect to them too

# right now the gui can only receive one message and has to send one before being able
# to receive anohter. Check why that is.

class MorseTransmitter(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        self.timer = MorseTransmissionTimer()

        self.btn_transmit.pressed.connect(self._btn_transmit_pressed)
        self.btn_transmit.released.connect(self._btn_transmit_released)

        self.btn_clear.clicked.connect(self._btn_clear)
        self.btn_start_host.clicked.connect(self._btn_start_host)
        self.btn_connect.clicked.connect(self._btn_connect)

        self.current_letter = ""
        self.space_detector = 0

        local_ip = create_local_ip()
        self.ledit_local_ip.setText(local_ip)
        self.server_thread = ServerThread(local_ip, 5050)
        self.server_thread.client_connected.connect(self._client_connected)
        self.server_thread.message_received.connect(self._receive_message)
        self.server_thread.message_clear.connect(self._receive_message_clear)

    def _btn_start_host(self):
        """ Begins the transmitter's server for another transmitter to connect
        to."""
        self.server_thread.start()
        self.ledit_connection_status.setText("server started...")

    def _client_connected(self):
        """ Upon a successful connection, signals user with an updated text."""
        self.ledit_connection_status.setText("client connected")

    def _receive_message(self, message):
        """ Handles the message_received signal when the transmitter receives
        a message and places it into the received message box.
        """
        self.pte_message_recv.insertPlainText(message)

    def _receive_message_clear(self):
        """ Handles the message_clear signal when the transmitter receives
        the prompt to clear the received message box.
        """
        self.pte_message_recv.clear()

    def _connection_closed(self):
        """ The closing of the server and client is handled in the thread so
        this function is mainly for other visual operations.
        """
        print("connection_closed")
        self.ledit_connection_status.setText("None")

    def _btn_transmit_pressed(self):

        self.timer.start_timer()

    def _btn_transmit_released(self):

        self.timer.end_timer()
        transmission = self.timer.transmission()
        # self.pte_message_sent.insertPlainText(transmission)
        self.current_letter += transmission

        # if left for a dash amount of time add anohter space

    # need to distinguish hte end of a letter with the end of a word by lenght of time
    def _space(self):
        self.timer.reset()
        self.timer.start_timer()

        while True:
            time.sleep(0.02) # time samples
            if self.timer.current_time() >= self.timer.dash_length:
                self.pte_message_sent

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
    # app.setStyleSheet(Path('ui/breeze_dark.qss').read_text())
    window = MorseTransmitter()
    window.show()
    sys.exit(app.exec_())
