import sublime_plugin
import sublime
import socket
import select
from threading import Thread
import queue


PORT = 8008


class Assistant(sublime_plugin.EventListener):

    def __init__(self):
        print("init")
        self.suggestions = []
        self.last_update = 0
        try:
            self.connection = ConnectionHandler()
        except ConnectionRefusedError:
            self.connection = None
            sublime.error_message("Connecting to Kronus server failed")
        else:
            self.connection.start()

            def __del__(self):
                print("alma")
                self.connection.__del__()

    def on_modified_async(self, view: sublime.View):
        if self.connection:
            # content = view.substr(sublime.Region(0, view.size()))
            count = view.change_count()
            self.connection.message_queue.put_nowait(str(count))

    def on_query_completions(self, view, prefix, locations):
        if view.change_count() != self.last_update:
            self.get_suggestions()
            self.last_update = view.change_count()
        # print(prefix)
        print(self.suggestions)
        return self.suggestions

    def get_suggestions(self):
        if self.connection:
            self.connection.message_queue.put_nowait("get")
            try:
                data = self.connection.suggestion_queue.get(True, 0.001)
            except queue.Empty:
                print("No reply")
            else:
                print(data)
                self.suggestions = [(data + "\tKronus", data)]


class ConnectionHandler(Thread):

    def __init__(self):
        super().__init__()
        self.message_queue = queue.Queue()
        self.suggestion_queue = queue.Queue()
        print("Initialize connection")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((socket.gethostname(), PORT))

    def run(self):
        inout = [self.socket]
        while True:
            read_feeds, write_feeds, exception_feeds = select.select(inout, inout, [])
            for read in read_feeds:
                data = read.recv(1024)
                print(data.decode())
                self.suggestion_queue.put(data.decode())
            for write in write_feeds:
                try:
                    next_msg = self.message_queue.get_nowait()
                except queue.Empty:
                    pass
                else:
                    write.send(next_msg.encode())
            for exception in exception_feeds:
                print(exception)  # TODO: handle exception

    def __del__(self):
        print("Close socket")
        self.socket.close()
