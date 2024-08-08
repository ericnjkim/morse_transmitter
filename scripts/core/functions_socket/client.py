import socket
import threading


class Client():

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        self.client.connect((self.server_host, self.server_port))

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_messages)
        send_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode("utf-8")
                print(message)
            except:
                print("Error")
                self.client.close()
                break

    def send_messages(self):
        while True:
            message = input("")
            if message == "/disconnect":
                self._disconnect_client()
                break
            self.client.send(message.encode("utf-8"))

    def _disconnect_client(self):
        self.client.send("/disconnect".encode("utf-8"))
        print("Disconnecting...")
        self.client.close()


host = socket.gethostbyname(socket.gethostname())
port = 5050
client = Client(host, port)
client.start_client()