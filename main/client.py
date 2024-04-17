# Import packages
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234


def server_listening(client):
    while True:
        message = client.recv(2048).decode('utf-8')

        if message:
            print(f'{message}')
            # sender_name, message_context = message.split('~')[0], message.split('~')[1]
            # Message from server:
            # print(f'[{sender_name}]~{message_context}')


def sending_message_to_server(client):
    """ Send message to server from client input """
    while True:
        message = input().strip()
        if message:
            client.sendall(message.encode())
        else:
            print('Message should not be empty')


def start_communication(client):
    while True:
        username = input('Enter username: ')
        if len(username := username.strip()):

            print("=== Instruction ===\n" +
                  '1. To send broadcast message: @broadcast~context_of_your_message\n'+
                  '2. To send message to single client directly: @client_name~context_of_your_message\n'+
                  '='*20)
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
