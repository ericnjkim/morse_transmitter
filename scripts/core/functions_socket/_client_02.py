import socket
import threading
import os
import sys


class Client(threading.Thread):

    def __init__(self, server_host, server_port):
        super().__init__()
        self.server_host = server_host
        self.server_port = server_port
        self.id = ""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.client_socket.connect((self.server_host, self.server_port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode("utf-8")
                print(message)
            except:
                print("Error")
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            message = input("")
            if message == "/quit":
                self.client_socket.send("Recipient disconnected".encode("utf-8"))
                self.client_socket.close()
                print("Disconnected")
                os._exit(0)
                break
            self.client_socket.send(message.encode("utf-8"))



#     def run(self):
#
#         while True:
#             if message == "/quit":
#                 self.socket.sendall(f"{self.name} has disconnected".encode("utf-8"))
#                 print("Quitting...")
#                 self.socket.close()
#                 os._exit(0)
#                 break
#             self.socket.sendall(message.encode("utf-8"))
#
# class ClientReceiver(threading.Thread):
#
#     def __init__(self, socket, name):
#         super().__init__()
#
#         self.socket = socket
#         self.name = name
#         self.messages = []
#
#     def run(self):
#         while True:
#             message = self.socket.recv(1024).decode("utf-8")
#
#             if message:
#                 print(message)
#                 self.messages.append(message)
#
#             else:
#                 print("lost connection to server")
#                 print("Quitting...")
#                 self.socket.close()
#                 os._exit(0)
#
#
# class Cient()




host = socket.gethostbyname(socket.gethostname())
port = 5050
client = Client(host, port)
client.start()