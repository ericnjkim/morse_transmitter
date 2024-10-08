
import os
import sys
import threading
from datetime import datetime
from pathlib import Path
import logging
import socket

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog

from server_thread import ServerThread
from client_thread import ClientThread
from message_dialog import MessageDialog

from functions_morse_translator import translate


UI_FILE = f"{os.path.dirname(__file__)}/ui/morse_transmitter_main.ui"


class MorseTransmitter(QtWidgets.QWidget):
    """ The main widget that ties the rest of the scripts together. Running an
    instance of this class will begin the tool.
    """
    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        # connect buttons
        self.btn_dot.clicked.connect(self._btn_dot)
        self.btn_dot.setShortcut(QtGui.QKeySequence("."))
        self.btn_dash.clicked.connect(self._btn_dash)
        self.btn_dash.setShortcut(QtGui.QKeySequence(","))
        self.btn_slash.clicked.connect(self._btn_slash)
        self.btn_slash.setShortcut(QtGui.QKeySequence("/"))
        self.btn_clear.clicked.connect(self._btn_clear)
        self.btn_start_host.clicked.connect(self._btn_start_host)
        self.btn_connect.clicked.connect(self._btn_connect)
        self.btn_disconnect.clicked.connect(self._btn_disconnect)
        self.btn_disconnect.hide()

        # working variables
        self.current_letter = ""
        self.space_detector = 0
        self.host_or_connector = 0

        # default widget disablings
        self.btn_disconnect.setEnabled(0)

        # default parameters
        local_ip = socket.gethostbyname(socket.gethostname())
        port = "5050"
        self.ledit_local_ip.setText(local_ip)
        self.ledit_local_port.setText(port)
        self.ledit_receiver_port.setText(port)

        # Qthread initialisations
        self.server_thread = ServerThread(local_ip, port)

        self.client_thread = ClientThread(local_ip, port, 0)
        self.client_thread.message_received.connect(self._receive_message)
        self.client_thread.message_clear.connect(self._receive_message_clear)
        self.client_thread.status_log.connect(self._handle_status_log)

    # _____functions for retrieving values_____
    def _get_local_address(self) -> tuple:
        return (self.ledit_local_ip.text(), int(self.ledit_local_port.text()))

    def _get_receiver_address(self) -> tuple:
        return (self.ledit_receiver_ip.text(), int(self.ledit_receiver_port.text()))

    def _local_address_populated(self) -> bool:
         return (self.ledit_local_ip.text() and self.ledit_local_port.text())

    def _receiver_address_populated(self) -> bool:
         return (self.ledit_receiver_ip.text() and self.ledit_receiver_port.text())

    # _____functions for connection buttons_____
    def _btn_start_host(self) -> None:
        """ Begins the transmitter's server for another transmitter to connect
        to."""
        # end early if parameters are not filled
        if not self._local_address_populated():
            msg = "Local address not fully populated.\nCannot host."
            dlg = MessageDialog(msg)
            dlg.exec()
            return
        _, local_port = self._get_local_address()
        self.server_thread.port = local_port
        self.server_thread.start()

        self.client_thread.server_port = local_port
        self.client_thread.start()
        self.btn_connect.setEnabled(0)
        self.btn_start_host.setEnabled(0)
        self.btn_disconnect.setEnabled(1)

        self.host_or_connector = 0
        self._handle_status_log("hosting")

    def _btn_connect(self) -> None:
        """ Initiates the connection between the local transmitter and a target
        transmitter.
        """
        # end early if parameters are not filled
        if not self._receiver_address_populated():
            msg = "Receiver address not fully populated.\nCannot connect."
            dlg = MessageDialog(msg)
            dlg.exec()
            return
        receiver_ip, receiver_port = self._get_receiver_address()
        # have some sort of check if the ip was valid or not.
        self.client_thread.server_host = receiver_ip
        self.client_thread.server_port = receiver_port
        self.client_thread.start()

        self.btn_start_host.setEnabled(0)
        self.btn_connect.setEnabled(0)
        self.btn_disconnect.setEnabled(1)
        self.host_or_connector = 1

    def _btn_disconnect(self):
        self.btn_disconnect.setEnabled(0)
        self.btn_connect.setEnabled(1)
        self.btn_start_host.setEnabled(1)
        self.server_thread.close_server()
        self.client_thread.disconnect()

    # _____functions for signal handling_____
    def _handle_status_log(self, message) -> None:
        """ Upon a successful connection, signals user with an updated text."""
        self.ledit_connection_status.setText(message)

    def _receive_message(self, message) -> None:
        """ Handles the message_received signal and pastes text into box."""
        print(f"received message {message}")
        self.pte_message_recv.insertPlainText(message)

    def _receive_message_clear(self) -> None:
        """ Handles the message_clear signal and clears message box."""
        self.pte_message_recv.clear()

    # _____functions for morse typing buttons_____
    def _btn_dot(self) -> None:
        self.current_letter += "."

    def _btn_dash(self) -> None:
        self.current_letter += "_"

    def _btn_slash(self) -> None:
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
            self._transmit_message(character)
            self.current_letter = ""
            self.space_detector = 0

    def _btn_clear(self) -> None:
        """ Clears the sent message text window."""
        self.pte_message_sent.clear()
        self._transmit_message("/clear")
        self.space_detector = 0

    def _transmit_message(self, message):
        """ If a receiver is present, transmit message."""
        if ((self.host_or_connector == 0 and self.server_thread.server_full())
            or (self.host_or_connector == 1 and self.client_thread.connected_to_server)):
            self.client_thread.send_message(message)


def _logger_setup() -> logging.Logger:
    """ Module level logger setup to help with dev and debug on server
    thread.
    """
    logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(format="%(asctime)s: %(module)s: %(levelname)s: %(funcName)s: %(message)s")
    logger = logging.getLogger(__name__)
    print("logger_setup")
    return logger


def run():
    _logger_setup()
    app = QApplication(sys.argv)
    qss_path = os.path.dirname(__file__) + "/qss/dark.qss"
    app.setStyleSheet(Path(qss_path).read_text())
    window = MorseTransmitter()
    window.show()
    sys.exit(app.exec_())

run()