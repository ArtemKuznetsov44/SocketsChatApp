import socket
from select import select

# Precursors for colling gen-functions in tasks list:
to_read = {}
to_write = {}

# Our list for keeping tasks - generator-functions:
tasks = []


def server_creation():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5000))
    server.listen()

    while True:
        # Blocking function, server socket waits for incoming data:
        yield ('read', server)
        client, address = server.accept()  # READ

        # Add next gen-function as task into tasks list:
        tasks.append(client_communication(client))


def client_communication(client: socket.socket):
    while True:
        # Blocking function, client socket waits for incoming data:
        yield ('read', client)
        request = client.recv(2048)  # READ

        if request == b'\n':
            client.close()
            break
        else:
            response = 'Hello from server!\n'.encode()
            # Blocking function, client socket write data:
            yield ('write', client)
            client.send(response)  # WRITE


def event_loop():
    while any([to_read, to_write, tasks]):

        # ONLY IF TASKS LIST IS EMPTY:
        while not tasks:
            ready_to_read_socks, ready_to_write_socks, _ = select(to_read, to_write, [])

            for sock in ready_to_read_socks:
                # to_read[sock] - returns gen-function where socket is ready to read data:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write_socks:
                # to_read[sock] - returns gen-function where socket is ready to write data:
                tasks.append(to_write.pop(sock))

        # When we have tasks in our tasks-list:
        try:
            # Pop the first one:
            task = tasks.pop(0)
            # Gen-function will return the tuple as ('reason', socket_obj):
            reason, socket_obj = next(task)

            # Code for add data into dictionaries:
            if reason == 'read':
                to_read[socket_obj] = task
            if reason == 'write':
                to_write[socket_obj] = task

        except StopIteration:
            print('Everything is done!')


if __name__ == '__main__':
    # Add our first gen-function-tasks into list:
    tasks.append(server_creation())
    event_loop()
