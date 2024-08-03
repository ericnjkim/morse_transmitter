import socket


def start_client(host, port: int=5050):
    # host = socket.gethostbyname(socket.gethostname())
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    while True:
        client.send(input("Message: ").encode("utf-8"))
        message = client.recv(1024).decode("utf-8")
        if message == "/close":
            break
        else:
            print(message)

    client.close()


if __name__ == "__main__":
    start_client("192.168.25.173")
# print("init client")
# start_client()