import sublime_plugin
import sublime

import socket
import struct
import textwrap

PORT = 8008
string_size = 1024
serializer = struct.Struct('I ' + str(string_size) + 's')


class Assistant(sublime_plugin.EventListener):

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((socket.gethostname(), PORT))
        self.last_change = 0
        self.list = []

    def on_query_completions(self, view, prefix, locations):
        if self.last_change != view.change_count():
            self.last_change = view.change_count()
            # print(view.sel())
            pos = view.sel()[0].begin()
            parts = textwrap.wrap(view.substr(sublime.Region(0, view.size())), string_size)
            part_count = len(parts)
            for ind, prt in enumerate(parts):
                self.socket.send(serializer.pack(part_count - ind, bytes(prt, 'utf-8')))
            self.socket.send(serializer.pack(0, bytes(str(pos), 'utf-8')))
            self.list = []
            data = serializer.unpack(self.socket.recv(serializer.size))
            while data[0] > 0:
                suggestion = data[1].decode('utf-8').rstrip('\x00')
                self.list.append((suggestion + "\tKrous", suggestion))
                data = serializer.unpack(self.socket.recv(serializer.size))
        return self.list