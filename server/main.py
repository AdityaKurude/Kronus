import socket
from threading import Thread

PORT = 8009
NUMBER_OF_CONNECTIONS = 10


class Worker(Thread):

    def __init__(self, socket, address):
        super().__init__()
        self.socket = socket
        self.address = address
        self.run()

    def run(self):
        while True:
            # TODO: optimize communication mechanism
            message = self.socket.recv(1024).decode()
            print(message)
            # TODO: handle multiple suggestions
            self.socket.send("Just_give_up,_It_wont_work".encode())

    # handle graceful thread closing


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server.bind((socket.gethostname(), PORT))
print("Binding server to %i" % PORT)

server.listen(NUMBER_OF_CONNECTIONS)

workers = []

while True:
    client, address = server.accept()
    workers.append(Worker(client, address))
