import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((socket.gethostname(), 5051))
HEADER_SIZE = 10
# the buffer represents the size of the data package sent or received
while True:
    full_msg = ""
    new_msg = True

    full_msg = ""
    while True:
        msg = server.recv(100) # a received message from the server up to 1024 bytes
        # prevent processing empty string
        if new_msg:
            print(f"new message length: {msg[:HEADER_SIZE]}")
            msglen = int(msg[:HEADER_SIZE])
            new_msg = False

        full_msg += msg.decode("utf-8")

        # confirm that the received message is the size that the header states
        # if so we can be assured we've received the whole message.
        if len(full_msg) - HEADER_SIZE == msglen:
            print("full msg received")
            print(full_msg)
            new_msg = True

    print(full_msg)