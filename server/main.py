import socket
import select
import queue
import struct

PORT = 8008
string_size = 1024
serializer = struct.Struct('I ' + str(string_size) + 's')


def autocomplete(context, pos):
    print(context)
    print(pos)
    return ["Justgiveup", "Yousuck"]


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
        self.connection.send(message)


class Server():

    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setblocking(0)
        self.server.bind((socket.gethostname(), PORT))
        print("Binding server to %i" % PORT)  # TODO: shod use logging
        self.server.listen(5)

    def fileno(self):
        return self.server.fileno()

    def new_connection(self):
        connection, client_address = self.server.accept()
        return Connection(connection, client_address)

    def close(self):
        self.server.close()


server = Server(PORT)

inputs = [server]
outputs = []
message_queues = {}

parts = []

while True:
    try:
        read_feeds, write_feeds, exception_feeds = select.select(inputs, outputs, inputs)
        for read in read_feeds:
            if read is server:
                connection = read.new_connection()
                print("Client connected.")
                inputs.append(connection)
                message_queues[connection] = queue.Queue()
            else:
                data = read.get_message(serializer.size)
                if data:
                    data = serializer.unpack(data)
                    if data[0] == 0:
                        pos = data[1].decode().rstrip('\x00')
                        context = ''.join(parts)
                        suggestions = autocomplete(parts, pos)
                        sug_count = len(suggestions)
                        for ind, sug in enumerate(suggestions):
                            message_queues[read].put_nowait(serializer.pack(sug_count - ind, bytes(sug, 'utf-8')))
                        message_queues[read].put_nowait(serializer.pack(0, bytes("", 'utf-8')))
                        if read not in outputs:
                            outputs.append(read)
                    else:
                        parts.append(data[1].decode('utf-8').rstrip('\x00'))
                else:
                    print("Client disconnected.")
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
    except KeyboardInterrupt:
        print("\nStopping server")
        break
for input in inputs:
    input.close()