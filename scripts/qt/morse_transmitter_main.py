import os
import sys
from datetime import datetime

from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QDialog

from scripts.core.functions_morse_translator import translate

UI_FILE = f"{os.path.dirname(__file__)}/ui/morse_transmitter_main.ui"
# if os.path.exists(UI_FILE):
#     print("test")


class MorseTransmitter(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        self.btn_dot.clicked.connect(self._btn_dot)
        self.btn_dash.clicked.connect(self._btn_dash)
        self.btn_slash.clicked.connect(self._btn_slash)
        self.btn_clear.clicked.connect(self._btn_clear)

        self.current_letter = ""
        self.space_detector = 0

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # # set style
    window = MorseTransmitter()
    window.show()
    sys.exit(app.exec_())

    # btn = QtWidgets.QPushButton()
    # [print(i) for i in dir(btn)]