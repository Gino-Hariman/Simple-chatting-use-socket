import socket
import select

HEADER = 24
IP = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

PORT = 7777

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# FOR RECONNECT
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((IP, PORT))
server.listen()

sockets_list = [server]

clients = {}

print(f'Listening for connetions on {IP}:{PORT}...')


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER)

        if not len(message_header):
            return False

        message_length = int(message_header.decode(FORMAT).strip())

        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    # untuk mengecek socket baru
    for notified_socket in read_sockets:
        if notified_socket == server:
            client_socket, client_address = server.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"{user['data'].decode(FORMAT)} joined the room. ")
            print(
                f"Accepted new connection from {client_address}:{client_address[1]} \nname: {user['data'].decode(FORMAT)}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(
                    f"{clients[notified_socket]['data'].decode(FORMAT)} Exited Room.")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(
                f"{user['data'].decode(FORMAT)} > {message['data'].decode(FORMAT)}")

            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(
                        user['header'] + user['data'] + message['header'] + message['data'])

    # jika socket disconnect
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
