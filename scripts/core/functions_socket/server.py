import threading
import socket
import os

"""
Sockets are categorised as either listening or connecting sockets. Here the 
server has a listening socket but every time a connection_socket connects, it will create
a new socket for sending and receiving data.
"""


class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.connection_map = {}
        self.connections = []
        # create server socket with internet streaming capabilities
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # have socket set to reuse address rather than naturally expire.
        # this will prevent the whole "This port is already in use" thing.
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.commands = ["/disconnected"]

    def run(self):
        print("starting server...")
        self.server.bind((self.host, self.port))
        self.server.listen(2)

        while True:
            connection_socket, address = self.server.accept()
            if len(self.connection_map) == 2:
                connection_socket.sendall(f"This connection is occupied.".encode("utf-8"))
                continue

            print(f"Connected: {str(address)}")
            self.connection_map[connection_socket] = address
            self.broadcast(f"/server_status connection:{self.connection_map[connection_socket]}")
            connection_socket.send("/connection_socket_status successful connection".encode("utf-8"))

            # attaching the handle function with the connection_socket as an argument on a unique thread

            receive_message_thread = threading.Thread(target=self.receive_message, args=(connection_socket,))
            receive_message_thread.start()

    def broadcast(self, message, author=None):
        for connection_socket in self.connection_map:
            # exclude sender from broadcast
            if author == connection_socket:
                continue
            connection_socket.send(message.encode("utf-8"))

    def receive_message(self, connection_socket):
        while True:
            try:
                message = connection_socket.recv(1024).decode("utf-8")
                if message == "/disconnect":
                    self.connection_map.pop(connection_socket)
                    self.broadcast(f"/receiver_disconnected", connection_socket)
                    continue
                self.broadcast(f"{self.connection_map[connection_socket]}: {message}", connection_socket)
            except:
                connection_socket.close()
                self.broadcast(f"/server_status disconnection:{self.connection_map[connection_socket]}")
                self.connection_map.pop(connection_socket)
                break

def server_commands(server):
    print("server commands now active")
    while True:
        input_text = input("")
        if input_text == "/close":
            print("Ending all connections...")
            for connection in server.connection_map:
                connection.close()
            print("Shutting down server")
            os._exit(0)


host = socket.gethostbyname(socket.gethostname())
port = 5050
server = Server(host, port)
server.start()
server_commands_thread = threading.Thread(target=server_commands, args=(server,))
server_commands_thread.start()
