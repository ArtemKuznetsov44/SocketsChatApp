# Import packages
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234


def server_listening(client):
    while True:
        message = client.recv(2048).decode('utf-8')
        if message:
            sender_name, message_context = message.split('~')[0], message.split('~')[1]
            print(f'[{sender_name}] {message_context}')


def sending_message_to_server(client):
    while True:
        message = input('Message to send: ').strip()
        if message:
            client.sendall(message.encode())
        else:
            print('Message should not be empty')


def start_communication(client):
    while True:
        username = input('Enter username: ')
        if len(username := username.strip()):
            client.sendall(username.encode())
            break

    threading.Thread(target=server_listening, args=(client,)).start()

    sending_message_to_server(client)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print('Successfully connected to server on {}:{}'.format(HOST, PORT))
    except socket.error:
        print('Could not connect to server')
        exit()

    start_communication(client)

    # threading.Thread(target=server_listening, args=(client,)).start()
    # sending_message_to_server(client)


if __name__ == '__main__':
    main()
