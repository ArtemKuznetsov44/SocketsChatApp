# Import packages for work
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234  # from 0 to 65355, as far as I remember
clients_socket_username = {}
clients_username_socket = {}

# The main socket logic is, who send, those will receive!
# Sending for socket is not the same sending as well. So when we send, we write data into the current socket buffer.
# One socket - one buffer, so who send, those can read this data from buffer


def send_to_single_client(client, message):
    """ Send a message to the single client """
    client.sendall(message.encode())


def send_to_all_clients(message):
    """ Method to send message to all clients"""

    for client, _ in clients_socket_username.items():
        send_to_single_client(client, message)


def listen_for_messages(client, username):
    """ Here server listen client messages """

    while True:

        message = client.recv(2048).decode('utf-8').strip()

        if message:
            message_for_all = username + '~' + message
            send_to_all_clients(message_for_all)
        else:
            pass


def client_handler(client, address):
    """ Method to handle client connection only should:
     1. Receive the client message
     2. Get the nickname and make association with socket
     3. Current thread will be killed, so we open new thread for client wor listening messages"""

    while True:
        username = name.strip() if (name := client.recv(2048).decode('utf-8')) else None

        if username:
            clients_socket_username[client] = username
            # clients_username_socket[username] = client
            print('Username for client with address {} was set successfully: {}'.format(address, username))
            send_to_all_clients(f'SERVER~{username} joined to the chat!')
            break
        # else:
        #     print('Client send invalid username')

    threading.Thread(target=listen_for_messages, args=(client, username)).start()


def main():
    """ Main function should:
    1. Create the server socket instance
    2. Bind this socket with address and port
    3. Listen for client connection
    4. On every client connection, log it and open new thread for work with client """

    # Socket instance creation:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Binding current socket with HOST:PORT:
    try:
        server.bind((HOST, PORT))
    except socket.error:
        print('Server socket bing error')
        exit()

    # Open for listening connections:
    server.listen()
    print('Server is listening on {}:{}'.format(HOST, PORT))

    while True:
        # Accepting incoming connections:
        client, address = server.accept()
        print('Accepted connection from {}'.format(address))

        # Start new thread to work with client:
        threading.Thread(target=client_handler, args=(client, address)).start()


if __name__ == '__main__':
    main()
