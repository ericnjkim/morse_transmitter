import os
import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from scripts.qt.morse_transmitter_main import MorseTransmitter

def run():
    """ Function to begin running the gui."""
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('qt/material_dark.qss').read_text())
    window = MorseTransmitter()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()