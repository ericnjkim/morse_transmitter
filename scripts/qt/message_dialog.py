import os
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication


UI_FILE = f"{os.path.dirname(__file__)}/ui/message_dialog.ui"


class MessageDialog(QtWidgets.QDialog):
    """ This widget is to be used as a generic message prompt to alert or
    inform the user in any way.
    """
    def __init__(self, text):
        super().__init__()

        uic.loadUi(UI_FILE, self)

        self.label_message.setText(text)
        self.btn_close.clicked.connect(self.close)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MessageDialog("mes")
    window.show()
    sys.exit(app.exec_())