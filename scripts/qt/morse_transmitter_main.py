import os
import sys
import threading
from datetime import datetime
import logging
import socket

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog

from server_thread import ServerThread
from client_thread import ClientThread

# allows to import from parent directory
if '..' not in sys.path: sys.path.append('..')

from core.functions_morse_translator import translate


UI_FILE = f"{os.path.dirname(__file__)}/ui/morse_transmitter_main.ui"

# - See if I can get the morse buttons to be replaced with a single button and
# work off timing for dots and dashes.
# if someone connects to this server, immediately connect to them too

# right now the gui can only receive one message and has to send one before being able
# to receive anohter. Check why that is.

# connection status needs updating
# closing connection needs working on as well
# manual port writing

class MorseTransmitter(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        self.btn_dot.clicked.connect(self._btn_dot)
        self.btn_dot.setShortcut(QtGui.QKeySequence("."))
        self.btn_dash.clicked.connect(self._btn_dash)
        self.btn_dash.setShortcut(QtGui.QKeySequence(","))
        self.btn_slash.clicked.connect(self._btn_slash)
        self.btn_slash.setShortcut(QtGui.QKeySequence("/"))
        self.btn_clear.clicked.connect(self._btn_clear)
        self.btn_start_host.clicked.connect(self._btn_start_host)
        self.btn_connect.clicked.connect(self._btn_connect)

        self.current_letter = ""
        self.space_detector = 0
        self.host_or_connector = 0

        local_ip = socket.gethostbyname(socket.gethostname())
        self.ledit_local_ip.setText(local_ip)

        self.server_thread = ServerThread(local_ip, 5051)
        self.server_thread.client_connected.connect(self._client_connected)
        # self.server_thread.message_received.connect(self._receive_message)
        # self.server_thread.message_clear.connect(self._receive_message_clear)

        self.client_thread = ClientThread(local_ip, 5051, 0)
        self.client_thread.message_received.connect(self._receive_message)
        self.client_thread.message_clear.connect(self._receive_message_clear)


    def _btn_start_host(self):
        """ Begins the transmitter's server for another transmitter to connect
        to."""
        self.server_thread.start()
        self.ledit_connection_status.setText("server started...")

        self.client_thread.start()
        self.btn_connect.setEnabled(0)
        self.host_or_connector = 0

    def _client_connected(self):
        self.ledit_connection_status.setText("client connected")

    def _receive_message(self, message):
        """ Handles the message_received signal when the transmitter receives
        a message and places it into the received message box.
        """
        print(f"received message {message}")
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
        self.client_thread
        self.ledit_connection_status.setText("None")

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
            self._transmit_message(" ")
            self.space_detector = 0
            return None

        character = translate(self.current_letter)
        if character:
            self.pte_message_sent.insertPlainText(character)
            print("character writing" + character)
            self._transmit_message(character)
            self.current_letter = ""
            self.space_detector = 0

    def _transmit_message(self, message):

        if ((self.host_or_connector == 0 and self.server_thread.server_full())
            or (self.host_or_connector == 1 and self.client_thread.connected_to_server)):
            print("TRANSMITTING "+ message)
            self.client_thread.send_message(message)


    def _btn_clear(self):
        """ Clears the sent message text window."""
        self.pte_message_sent.clear()
        self._transmit_message("/clear")
        self.space_detector = 0

    def _btn_connect(self):
        """ Initiates the connection between the local transmitter and a target
        transmitter.
        """
        receiver_ip = self.ledit_receiver_ip.text()
        # have some sort of check if the ip was valid or not.
        self.client_thread.server_host = receiver_ip
        self.client_thread.server_port = 5051
        self.client_thread.start()

        self.btn_start_host.setEnabled(0)
        self.host_or_connector = 1



def _logger_setup() -> logging.Logger:
    """ Module level logger setup to help with dev and debug on server
    thread.
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(format="%(asctime)s: %(module)s: %(levelname)s: %(funcName)s: %(message)s")
    logger = logging.getLogger(__name__)
    # logger.setLevel(level="INFO")
    # formatter = logging.Formatter(
    #     "%(asctime)s: %(levelname)s: %(funcName)s: %(message)s")
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)
    print("logger_setup")
    return logger


# plaint text edit needs to be uneditable
def run():
    _logger_setup()
    app = QApplication(sys.argv)
    # app.setStyleSheet(Path('ui/breeze_dark.qss').read_text())
    window = MorseTransmitter()
    window.show()
    sys.exit(app.exec_())

run()