import socket

class Network:
    def __init__(self, server_ip="127.0.0.1", server_port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server_ip
        self.port = server_port
        self.connect()

    def connect(self):
        try:
            self.client.connect((self.server, self.port))
        except Exception as e:
            print(f"Unable to connect to server {self.server}:{self.port}: {e}")

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
