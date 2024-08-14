
import socket
import logging

from PyQt5.QtCore import QThread, pyqtSignal


logger = logging.getLogger(__name__)

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

class ClientThread(QThread):
    """ This class sends and receives messages and emits signals for the gui
    to use. It acts as the sockets for the gui.
    """
    message_received = pyqtSignal(str)
    message_clear = pyqtSignal()
    status_log = pyqtSignal(str)

    def __init__(self, server_host, server_port, id=0):
        super().__init__()
        self.server_host = server_host
        self.server_port = server_port
        self.id = id # will be set by server
        self.message_to_send = ""
        self.connected_to_server = False

        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.receive_thread = ClientReceiveThread(self)
        self.receive_thread.received_message.connect(self.handle_received_message)
        logger.debug("function complete")


    def run(self) -> None:
        """ Begins operations for connecting to a server and receiving data
        from it.
        """
        try:
            self.connection_socket.connect((self.server_host, self.server_port))
            self.receive_thread.start()
            self.connected_to_server = True
            self.status_log.emit("connection live")
        except:
            pass

    def send_message(self, message) -> None:
        """ Sends messages to the recipient via the connected server."""
        if message == "/quit":
            self.connection_socket.send("Recipient disconnected".encode("utf-8"))
            self.status_log.emit("disconnected")
            self.connection_socket.close()

        self.connection_socket.send(message.encode("utf-8"))

    def handle_received_message(self, message) -> None:
        """ Upon receiving a message through the ClientReceiveThread object,
        emit custom signals to be used in the main gui.
        """
        if message == "/clear":
            self.message_clear.emit()
        elif "/status_log" in message:
            status_log_message = message.split(":")[-1]
            self.status_log.emit(status_log_message)
        else:
            self.message_received.emit(message)
        logger.debug(f"received message: {message}")

    def disconnect(self) -> None:
        """ Disconnects the ClientThread from the server it's currently
        connected to.
        """
        self.connection_socket.close()
        self.status_log.emit("disconnected")


class ClientReceiveThread(QThread):
    """ This class act's as a receiver and is seperate to the ClientThread as
    the receiver needs to be constantly listening for incoming messages and
    so has it's own designated thread.
    """
    received_message = pyqtSignal(str)

    def __init__(self, client):
        super().__init__()
        self.client = client
        logger.debug("function complete")

    def run(self) -> None:
        """ Begins listening for incoming messages to the client's socket.
        If there are any errors on receiving message, disconnects from server.
        """
        while True:
            logger.debug(f"client message receiver active")

            try:
                message = self.client.connection_socket.recv(1024).decode("utf-8")
                if message:
                    logger.debug(f"message received: {message}")
                    self.received_message.emit(message)
            except:
                logger.debug(f"message failed to receive. disconnecting from server...")
                self.client.connection_socket.close()
                break
