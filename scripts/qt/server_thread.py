import sys
import socket
import os
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal


# try adding client handler into this qthread

""" Usually I'd prefer to have logic in the core directory but in this case I 
needed to wire the loop that received messages with a signal emitter.
"""

def _logger_setup() -> logging.Logger:
    """ Module level logger setup to help with dev and debug on server
    thread.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level="INFO")
    formatter = logging.Formatter(
        "%(asctime)s: %(levelname)s: %(funcName)s: %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    print("logger_setup")
    return logger

logger = logging.getLogger(__name__)

class ServerThread(QThread):
    """ Operations for the transmitter's ability to connect to another
    transmitter and for handling received messages.
    """
    # client_connected = pyqtSignal(tuple)
    client_connected = pyqtSignal()
    message_received = pyqtSignal(str)
    message_clear = pyqtSignal()
    connection_closed = pyqtSignal()

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

        self.connection_map = {} # socket, addr
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logging.debug(f"function completion")

    def run(self):

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        logger.debug(f"server socket listening...")

        while True:
            connection_socket, address = self.server_socket.accept()
            if len(self.connection_map) == 2:
                connection_socket.sendall(f"This connection is occupied.".encode("utf-8"))
                logger.warning(f"connection already occupied.")
                continue

            # print(f"Connected: {address}")
            logger.info(f"successful connection with new client: {address}")
            connection_id = len(self.connection_map) + 1
            self.connection_map[connection_id] = {"socket": connection_socket, "address": address}

            self.broadcast(f"/server_status connection:{address}")
            connection_socket.send("SERVER: successful connection".encode("utf-8"))

            server_socket = ServerSocketThread(connection_socket, connection_id, self)
            server_socket.start()

    def remove_connection(self, id):
        logger.debug(f"client connection to be removed: {id}")
        self.connection_map[id]["socket"].close()
        self.connection_map.pop(id)

            # message = client.recv(1024).decode("utf-8")
            # print("loop")
            # if message == "/close":
            #     print("close operation begun")
            #     client.close()
            #     server.close()
            #     self.connection_closed.emit()
            #     break
            # elif message == "/clear":
            #     print("clearing inbox")
            #     self.message_clear.emit()
            # else:
            #     print(message)
            #     self.message_received.emit(message)
            #     print("continue operation")


    def broadcast(self, message, sender_id=None):
        logger.debug(f"broadcasting: {message} from {sender_id}")
        for id in self.connection_map:
            if id != sender_id:
                self.connection_map[id]["socket"].send(message.encode("utf-8"))

    def close_server(self):
        logger.debug(f"server closing...")
        for id in self.connection_map:
            self.connection_map[id]["socket"].close()
        print("Server shutting down...")
        os._exit(0)

class ServerSocketThread(QThread):

    def __init__(self, socket_connection, id, server):
        super().__init__()
        self.socket_connection = socket_connection
        self.id = id
        self.server = server
        logger.debug(f"function completion")

    def run(self):
        while True:
            message = self.socket_connection.recv(1024).decode("utf-8")
            logger.debug(f"received message from {id}: {message}")

            if message:
                self.server.broadcast(message, self.id)
            else:
                logger.debug(f"connection closed with {id}")
                self.socket_connection.close()
                self.server.remove_connection(self.id)
                break

if __name__ == "__main__":
    import socket

    logger =_logger_setup()
    logger.setLevel(level="DEBUG")

    app = QApplication(sys.argv)

    local_ip = socket.gethostbyname(socket.gethostname())
    server_thread = ServerThread(local_ip, 5050)
    server_thread.start()

    sys.exit(app.exec_())