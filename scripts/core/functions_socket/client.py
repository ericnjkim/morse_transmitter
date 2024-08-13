import socket
import threading
import os


class Client(threading.Thread):

    def __init__(self, server_host, server_port):
        super().__init__()
        self.server_host = server_host
        self.server_port = server_port
        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.send_thread = threading.Thread(target=self.send_messages)

    def run(self):
        print("test")
        self.connection_socket.connect((self.server_host, self.server_port))
        print("Message sender active")
        # print("Message receiver active")
        self.receive_thread.start()
        self.send_thread.start()

    #
    def receive_messages(self):
        while True:
            try:
                message = self.connection_socket.recv(1024).decode("utf-8")
                print(message)
            except:
                self.close_socket()
                break

    def send_messages(self):
        while True:
            message = input("")
            if message == "/disconnect":
                self.close_socket()
                break
            self.connection_socket.send(message.encode("utf-8"))
    #
    def close_socket(self):
        try:
            self.connection_socket.send("Recipient disconnected".encode("utf-8"))
        except:
            pass
        print("Disconnecting...")
        self.connection_socket.close()
        os._exit(0)

host = socket.gethostbyname(socket.gethostname())
port = 5050
client = Client(host, port)
client.start()