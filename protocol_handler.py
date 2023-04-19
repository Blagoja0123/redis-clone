from socketserver import ThreadingMixIn as socket

class ProtocolHandler(object):
    def handle_request(self, socket_file):
        # parse request
        pass
    def write_response(self, socket_file, data):
        # serialize response data
        pass

