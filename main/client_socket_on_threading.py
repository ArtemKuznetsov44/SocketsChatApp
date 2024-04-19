import socket
import threading

HOST = '127.0.0.1'
PORT = 5000


def make_requests(client):
    while True:
        # Blocking
        message_to_send = input().strip()
        if '#' not in message_to_send or '::' not in message_to_send:
            print("Message in invalid format! Is must contain '#' and '::' symbols!")
            if not message_to_send[1:].strip('::'):
                print('Your message should have the context!')
        else:
            client.sendall(message_to_send.encode())


def client_init():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    while True:
        username = input('Enter you username as @<your_username>: ').strip()
        if username:
            client.send(username.encode())
            break

    # Start new thread for listen server responses:
    threading.Thread(target=server_listen, args=(client,)).start()
    # Run function with infinity-loop in main|current thread to give an opportunity to input messages:
    make_requests(client)


def server_listen(client):
    while True:
        # Blocking
        response = client.recv(2048)

        if not response:
            pass
        else:
            # Here we need to have the logic to send messages
            print(response.decode('utf-8'))


if __name__ == '__main__':
    client_init()
