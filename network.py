import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
        except Exception as e:
            print(f"Unable to connect to server: {e}")

    def send(self, data, receive=False):
        try:
            if isinstance(data, str):
                data = data.encode()
            self.client.send(data)
            if receive:
                return self.client.recv(2048)
            else:
                return None
        except socket.error as e:
            print(e)

    def recv(self):
        try:
            return self.client.recv(2048)
        except socket.timeout as e:
            return None
