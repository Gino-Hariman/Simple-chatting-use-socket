import socket
import select
import errno
import sys

HEADER = 24
IP = socket.gethostbyname(socket.gethostname())
PORT = 7777
FORMAT = 'utf-8'

my_username = input("Name: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))
client.setblocking(False)

username = my_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER}}".encode(FORMAT)
client.send(username_header + username)

while True:
    message = input(f'{my_username} > ')

    if message:
        message = message.encode(FORMAT)
        message_header = f"{len(message) :< {HEADER}}".encode(FORMAT)
        client.send(message_header + message)

    try:
        while True:
            # receive things
            username_header = client.recv(HEADER)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode(FORMAT).strip())
            username = client.recv(username_length).decode(FORMAT)

            message_header = client.recv(HEADER)
            message_length = int(message_header.decode(FORMAT).strip())
            message = client.recv(message_length).decode(FORMAT)

            print(f"{username} > {message} ")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('Error', str(e))
        sys.exit()
