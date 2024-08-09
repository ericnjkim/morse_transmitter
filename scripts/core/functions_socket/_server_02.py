import threading
import socket
import os

"""
Sockets are categorised as either listening or connecting sockets. Here the 
server has a listening socket but every time a client connects, it will create
a new socket for sending and receiving data.
"""


class Server(threading.Thread):

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
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
        print("server_listening")
        while True:
            client, address = self.server.accept()
            if len(self.connections) == 2:
                client.sendall(f"This connection is occupied.".encode("utf-8"))
                continue

            print(f"Connected: {str(address)}")
            self.connections.append(client)
            self.broadcast(f"/server_status connection:{address}")
            client.send("/client_status successful connection".encode("utf-8"))

            server_socket = ServerSocket(client, address, self)
            server_socket.start()
            self.connections.append(server_socket)
            print(f"ready to receive messages from {address}")

    def broadcast(self, message, author=None):
        for connection in self.connections:
            # exclude sender from broadcast
            if connection.sockname == author:
                continue
            connection.send(message.encode("utf-8"))

    # def remove_connection(self, connection):
    #     self.connections.remove(connection)

    # def receive_message(self, client):
    #     while True:
    #         try:
    #             message = client.recv(1024).decode("utf-8")
    #             if message == "/disconnect":
    #                 self.client_map.pop(client)
    #                 self.broadcast(f"/receiver_disconnected", client)
    #                 continue
    #             self.broadcast(f"{self.client_map[client]}: {message}", client)
    #         except:
    #             client.close()
    #             self.broadcast(f"/server_status disconnection:{self.client_map[client]}")
    #             self.client_map.pop(client)
    #             break

    # def handle_special_commands(self):

    # def server_commands(self):
    #     while True:
    #         prompt = input("")
    #         if prompt == "/close":
    #             self._close_server()
    #             break
    #         else:
    #             continue

    # def _close_server(self):
    #     print("closing server")
    #     # server.shutdown(socket.SHUT_RDWR)
    #     self.server.close()


class ServerSocket(threading.Thread):

    def __init__(self, socket_connection, socket_name, server):
        super().__init__()
        self.socket_connection = socket_connection
        self.socket_name = socket_name
        self.server = server

    def run(self):
        while True:
            message = self.socket_connection.recv(1024).decode("utf-8")

            if message:
                print(f"{self.socket_name}: {message}")
                self.server.broadcast(message, self.socket_name)
            else:
                print(f"{self.socket_name} has closed connection.")
                self.socket_connection.close()
                self.server.remove_connection(self)
                break

    def send(self, message):

        self.socket_connection.sendall(message.encode("utf-8"))

def exit(server):
    print("exit operation active")
    while True:
        input_text = input("")
        print(input_text)
        if input_text == "/close":
            print("Ending all connections...")
            for connection in server.connections:
                connection.socket_connection.close()
            print("Shutting down server")
            os._exit(0)



host = socket.gethostbyname(socket.gethostname())
port = 5050
server = Server(host, port)
server.start()
exit = threading.Thread(target=exit, args=(server,))
exit.start()