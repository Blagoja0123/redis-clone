from socketserver import ThreadingMixIn as socket
from socketserver import BaseServer as StreamServer
from socket import error as socket_error


from collections import namedtuple

from protocol_handler import ProtocolHandler

class CommandError(Exception): pass
class Disconnect(Exception): pass

Error = namedtuple('Error', ('message', ))

class Server(object):
    def __init__(self, host='127.0.0.1', port=31337, max_clients=32):
        self._pool = max_clients
        self._server = StreamServer(
            (host, port),
            self.connection_handler,
            spawn=self._pool
        )

        self._protocol = ProtocolHandler()
        self._kv = {}

    def connection_handler(self, conn, address):
        socket_file = conn.makefile('rwb')

        while True:
            try:
                data = self._protocol.handle_request(socket_file)
            except Disconnect:
                break
            try:
                resp = self.get_respone(data)
            except CommandError as exc:
                resp = Error(exc.args[0])

            self._protocol.write_response(socket_file, resp)

    def get_response(self, data):
        # unpack data
        pass

    def run(self):
        self._server.serve_forever()