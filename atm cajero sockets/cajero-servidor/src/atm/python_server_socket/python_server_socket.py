"""
Equivalente a lenin.java_server_socket.JavaServerSocket del profesor:
primer número = puerto donde escucha, segundo = tamaño de la cola de
conexiones pendientes (backlog). get() devuelve el socket ya en modo
"escuchando" (equivalente al ServerSocket de Java), o None si falló.
"""

import socket


class PythonServerSocket:

    def __init__(self, port: int, backlog: int):
        self.port = port
        self.backlog = backlog

    def get(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("0.0.0.0", self.port))
            server_socket.listen(self.backlog)
            return server_socket
        except OSError as e:
            print(f"Error creando el socket del servidor: {e}")
            return None
