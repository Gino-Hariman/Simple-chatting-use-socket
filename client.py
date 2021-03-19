import socket
import select
import errno
import sys

HEADER = 10
IP = '192.168.72.2'
PORT = 7777
FORMAT = 'utf-8'

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER}}".encode(FORMAT)
client_socket.send(username_header + username)

while True:
    message = input(f'{my_username} > ')

    if message:
        message = message.encode(FORMAT)
        message_header = f"{len(message) :< {HEADER}}".encode(FORMAT)
        client_socket.send(message_header + message)

    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode(FORMAT).strip())
            username = client_socket.recv(username_length).decode(FORMAT)

            message_header = client_socket.recv(HEADER)
            message_length = int(message_header.decode(FORMAT).strip())
            message = client_socket.recv(message_length).decode(FORMAT)

            print(f"{username} > {message} ")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
