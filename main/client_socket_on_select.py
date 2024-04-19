import socket
import sys
from select import select

HOST = '127.0.0.1'
PORT = 5000

to_monitor: list = [sys.stdin]


def client_init():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    to_monitor.append(client)
    return client


def receive_server_responses(client):
    response = client.recv(2048)

    if not response:
        pass
    else:
        print(response.decode('utf-8'))


def create_requests(client, context):
    request = context.encode()
    client.send(request)


def event_loop(client):
    while True:

        ready_to_read_objects, _, _ = select(to_monitor, [], [])

        for obj in ready_to_read_objects:
            if obj is client:
                receive_server_responses(obj)
            else:
                text = obj.readline().strip()
                create_requests(obj, text)


if __name__ == '__main__':
    client_sock = client_init()
    event_loop(client_sock)
