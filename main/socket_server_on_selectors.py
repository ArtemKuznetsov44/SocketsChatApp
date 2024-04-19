import socket
import selectors

HOST = '127.0.0.1'
PORT = 5000

selector = selectors.DefaultSelector()

active_clients_sock_name = {}
active_clients_name_sock = {}


def server_creation():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print('Server is listening on {}:{} for incoming connections...'.format(HOST, PORT))

    selector.register(fileobj=server, events=selectors.EVENT_READ, data=client_handler)


def client_handler(server_obj: socket.socket):
    client, addr = server_obj.accept()
    # client.sendall(b'Welcome to the server!\nPlease, enter your username: ')
    print('New client connected! Address is: {}'.format(addr))

    selector.register(fileobj=client, events=selectors.EVENT_READ, data=work_with_client)


def send_to_client_directly(recipient_username: str, sender_username: str, message: str):
    recipient_socket = active_clients_name_sock[recipient_username]
    recipient_socket.sendall(f'---> #incoming from {sender_username}::{message}'.encode())


def send_to_all_clients(sender_username: str, message: str):
    # Send to all others not including current client-sender:
    for c in active_clients_sock_name:
        c.sendall(f'^^^ #broadcast by {sender_username}:: {message}'.encode())


def work_with_client(client):
    request = client.recv(2048)

    if request == b'\n':
        client.close()
    else:
        # Here we work with client messages:
        message: str = request.decode('utf-8')

        if message.startswith('@'):

            username = message.strip()[1:]
            active_clients_sock_name[client] = username
            active_clients_name_sock[username] = client

            client.sendall('Welcome as full-chat member {}!\n'.format(username).encode())
            client.sendall('-> To send message broadcast: #broadcast::<your_message>\n'
                           '-> To send message directly: #<member_username>::<your_message>\n'
                           'Enjoy it! 🪐\n'.encode())

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


def event_loop():
    # Ween need to have an opportunities to accept incoming connections and receive clients' requests:
    while True:
        events = selector.select()

        for selector_key, _ in events:
            function = selector_key.data
            function(selector_key.fileobj)


if __name__ == '__main__':
    server_creation()
    event_loop()
