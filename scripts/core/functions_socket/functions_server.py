import socket
import threading

# create a socket of the ipv4 type that can stream
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 5050))

server.listen(5)

while True:
    client_socket, address = server.accept()
    print(f"[CONNECTED] {address}")
    client_socket.send(bytes("welcome to the server.", "utf-8"))