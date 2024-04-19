import socket
from select import select

HOST = '127.0.0.1'
PORT = 5000

to_monitor = []
active_clients_sock_name = {}
active_clients_name_sock = {}


def init_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()

    return server


def send_to_client_directly(recipient_username: str, sender_username: str, message: str):
    recipient_socket = active_clients_name_sock[recipient_username]
    recipient_socket.sendall(f'---> #incoming from {sender_username}::{message}'.encode())


def send_to_all_clients(sender_username: str, message: str):
    # Send to all others not including current client-sender:
    for c in active_clients_sock_name:
        c.sendall(f'^^^ #broadcast by {sender_username}:: {message}'.encode())


def client_handling(server):
    client, addr = server.accept()  # READ

    # This code now in client module:
    # client.sendall('Welcome to server!\nSpecify your USERNAME first with @<username>\n'.encode())
    to_monitor.append(client)


def work_with_client(client):
    request = client.recv(4096)  # READ

    if request == b'\n':
        client.close()
    else:
        message: str = request.decode('utf-8')

        if message.startswith('@'):

            username = message.strip()[1:]
            active_clients_sock_name[client] = username
            active_clients_name_sock[username] = client

            client.sendall('Welcome as full-chat member {}!\n'.format(username).encode())
            client.sendall('-> To send message broadcast: #broadcast::<your_message>\n'
                           '-> To send message directly: #<member_username>::<your_message>\n'
                           'Enjoy it! 😘\n==============\n'.encode())

            # Notify all clients that new users has connected with username:
            send_to_all_clients('SERVER', 'NEW USER HAS COME - {}'.format(username))

        elif message.startswith('#'):
            recipient, message_context = message.strip()[1:].split('::')

            if recipient == 'broadcast':
                sender_username = active_clients_sock_name.pop(client)
                send_to_all_clients(sender_username, message_context)
                active_clients_sock_name[client] = sender_username

            elif recipient in active_clients_name_sock:
                send_to_client_directly(recipient, active_clients_sock_name[client], message_context)


def event_loop(server):
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            if sock is server:
                client_handling(server)
            else:
                work_with_client(sock)


def main():
    server = init_server(HOST, PORT)
    print('Server is active and listening on {}:{}'.format(HOST, PORT))
    to_monitor.append(server)
    event_loop(server)


if __name__ == '__main__':
    main()
