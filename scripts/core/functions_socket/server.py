import threading
import socket


class Server():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_map = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.commands = ["/disconnected"]

    def start_server(self):
        print("starting server...")
        self.server.bind((self.host, self.port))
        self.server.listen(2)
        self.client_connecter()

    def broadcast(self, message, author=None):
        for client in self.client_map:
            # exclude sender from broadcast
            if author == client:
                continue
            client.send(message.encode("utf-8"))

    def client_connecter(self):
        while True:
            client, address = self.server.accept()
            if len(self.client_map) == 2:
                client.sendall(f"This connection is occupied.".encode("utf-8"))
                continue

            print(f"Connected: {str(address)}")
            self.client_map[client] = address
            self.broadcast(f"/server_status connection:{self.client_map[client]}")
            client.send("/client_status successful connection".encode("utf-8"))

            # attaching the handle function with the client as an argument on a unique thread
            server_commands_thread = threading.Thread(target=self.server_commands)
            server_commands_thread.start()
            receive_message_thread = threading.Thread(target=self.receive_message, args=(client,))
            receive_message_thread.start()

    def receive_message(self, client):
        while True:
            try:
                message = client.recv(1024).decode("utf-8")
                if message == "/disconnect":
                    self.client_map.pop(client)
                    self.broadcast(f"/receiver_disconnected", client)
                    continue
                self.broadcast(f"{self.client_map[client]}: {message}", client)
            except:
                client.close()
                self.broadcast(f"/server_status disconnection:{self.client_map[client]}")
                self.client_map.pop(client)
                break

    # def handle_special_commands(self):

    def server_commands(self):
        while True:
            prompt = input("")
            if prompt == "/close":
                self._close_server()
                break
            else:
                continue

    def _close_server(self):
        print("closing server")
        # server.shutdown(socket.SHUT_RDWR)
        self.server.close()

host = socket.gethostbyname(socket.gethostname())
port = 5050
server = Server(host, port)
server.start_server()
#
# # # testing a thing here
# def server_commands():
#     """ """
#     while True:
#         prompt = input("")
#         print(prompt)
#         if prompt == "/close":
#             print("closing server")
#             # server.shutdown(socket.SHUT_RDWR)
#             server.close()
#             break
#         else:
#             continue
#
#
