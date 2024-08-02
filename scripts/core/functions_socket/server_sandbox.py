import socket
import threading
import time

# create a socket of the ipv4 type that can stream
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 5051))
# print(socket.gethostname())
server.listen(5)

HEADER_SIZE = 10

while True:
    client_socket, address = server.accept()
    print(f"[CONNECTED] {address}")

    msg = "welcome to the server"
    # this will provide a header before the message itself which represents the
    # size of the incoming message.
    msg = f"{len(msg):<{HEADER_SIZE}}{msg}"
    client_socket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        msg = f"[TIMESTAMP]: {time.time()}"
        msg = f"{len(msg):<{HEADER_SIZE}}{msg}"
        client_socket.send(bytes(msg, "utf-8"))

    client_socket.close()
    #
    # import threading
    # import socket
    #
    # host = socket.gethostbyname(socket.gethostname())
    # print(host)
    # port = 5050
    #
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind((host, port))
    # server.listen()
    #
    # clients = []
    # nicknames = []
    #
    # client_map = {}
    #
    #
    # def broadcast(message):
    #     for client in client_map:
    #         client["client"].send(message)
    #
    #
    # def handle(client):
    #     while True:
    #         try:
    #             message = client["client"].recv(1024)
    #             broadcast(message)
    #         except:
    #             nickname = client["nickname"]
    #             client["client"].close()
    #             client_map.pop(client)
    #             broadcast(f"[DISCONNECTED]: {nickname}".encode("utf-8"))
    #             break
    #
    #
    # def receive():
    #     while True:
    #         client, address = server.accept()
    #         print(f"[CONNECTED]: {address}")
    #         client.send("nickname?".encode("utf-8"))
    #         nickname = client.recv(1024).decode("utf-8")
    #         client_map[address] = {"client": clients, "nickname": nickname}
    #         broadcast(f"[CONNECTED]: {nickname}".encode("utf-8"))
    #         client.send("[CONNECTED]: server".encode("utf-8"))