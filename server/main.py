import socket
import select
import queue

PORT = 8008


class Connection():

    def __init__(self, connection, client_address, nonblocking=True):
        self.connection = connection
        self.client_address = client_address
        if nonblocking:
            self.connection.setblocking(0)

    def fileno(self):
        return self.connection.fileno()

    def get_message(self, size=1024):
        return self.connection.recv(size)

    def close(self):
        self.connection.close()

    def send(self, message):
        self.connection.send(message.encode())


class Server():

    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(0)
        self.server.bind((socket.gethostname(), PORT))
        print("Binding server to %i" % PORT)  # TODO: shod use logging
        self.server.listen(5)

    def fileno(self):
        return self.server.fileno()

    def new_connection(self):
        connection, client_address = self.server.accept()
        return Connection(connection, client_address)


server = Server(PORT)

inputs = [server]
outputs = []
message_queues = {}

while True:
    read_feeds, write_feeds, exception_feeds = select.select(inputs, outputs, inputs)
    for read in read_feeds:
        if read is server:
            connection = read.new_connection()
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            data = read.get_message()
            if data:
                print(data.decode())
                if data.decode() == "get":
                    message_queues[read].put_nowait("Justgiveup")
                if read not in outputs:
                    outputs.append(read)
            else:
                if read in outputs:
                    outputs.remove(read)
                inputs.remove(read)
                read.close()
                del message_queues[read]
    for write in write_feeds:
        try:
            next_msg = message_queues[write].get_nowait()
        except queue.Empty:
            outputs.remove(write)
        else:
            write.send(next_msg)
    for ex in exception_feeds:
        inputs.remove(ex)
        if ex in outputs:
            outputs.remove(ex)
        ex.close()
        del message_queues[ex]
