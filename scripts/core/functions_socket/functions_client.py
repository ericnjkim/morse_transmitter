import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 5050))

msg = server.recv(1024) # a received message from the server up to 1024 bytes
print(msg.decode("utf-8"))