"""
Equivalente a lenin.java_client_socket.JavaClientSocket del profesor:
arma el socket.socket() y se conecta a host:puerto. get() devuelve
el socket conectado, o None si falló (igual que el Java original).
"""

import socket


class PythonClientSocket:

    def __init__(self, port: int, host: str):
        self.port = port
        self.host = host

    def get(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            return client_socket
        except OSError as e:
            print(f"Error creando el socket del cliente: {e}")
            return None
