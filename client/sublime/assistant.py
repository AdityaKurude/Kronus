import sublime_plugin
import sublime
import socket

PORT = 8009


class Assistant(sublime_plugin.EventListener):

    def __init__(self):
        self.connection = ConnectionHandler()

    def on_modified(self, view: sublime.View):
        # print(view.change_count())
        # print(view.symbols())
        # print(view.)
        self.suggestion = self.connection.send(
            view.substr(sublime.Region(0, view.size())))

    def on_query_completions(self, view, prefix, locations):
        print(prefix)
        return [(prefix, self.suggestion)]


class ConnectionHandler():

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((socket.gethostname(), PORT))

    def __del__(self):
        self.socket.close()

    def send(self, message):
        self.socket.send(message.encode())
        data = self.socket.recv(1024).decode()
        return data
