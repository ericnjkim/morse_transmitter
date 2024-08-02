import os
import sys
from datetime import datetime

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog

from scripts.core.functions_morse_translator import translate
from scripts.core.functions_socket.functions_client import start_client
from scripts.core.functions_socket.functions_server import start_server, create_local_ip

UI_FILE = f"{os.path.dirname(__file__)}/ui/morse_transmitter_main.ui"


# add keyboard inputs
# close off pte to manual typing
# add receiving message box

class MorseTransmitter(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        self.btn_dot.clicked.connect(self._btn_dot)
        self.btn_dash.clicked.connect(self._btn_dash)
        self.btn_slash.clicked.connect(self._btn_slash)
        self.btn_clear.clicked.connect(self._btn_clear)

        self.btn_connect.clicked.connect(self._btn_connect)

        self.current_letter = ""
        self.space_detector = 0

        self._start_host()

    def _start_host(self):
        # server seems to be stopping all other operations from running so it
        # needs to be on its own thread
        local_ip = create_local_ip()
        self.ledit_local_ip.setText(local_ip)
        # start_server(local_ip)

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