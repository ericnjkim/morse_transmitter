import threading
import socket

def create_local_ip() -> str:
    host = socket.gethostbyname(socket.gethostname())
    return host

def start_server(host: str=create_local_ip(), port: int=5050):
    port = 5050
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))

    print("Server started")

    server.listen()
    client, address = server.accept()
    # return client, address, server

    print("Server started")
    while True:
        message = client.recv(1024).decode("utf-8")
        if message == "/close":
            break
        else:
            print(message)

        client.send(input("Message: ").encode("utf-8"))

    client.close()
    server.close()



# print("started server")
# def handle_client(client, address, server):
#
#     while True:
#         message = client.recv(1024).decode("utf-8")
#         if message == "/close":
#             break
#         else:
#             print(message)
#
#         client.send(input("Message: ").encode("utf-8"))
#
#     client.close()
#     server.close()
# start_server()
