"""
Equivalente a lenin.server.Server del profesor.

Diferencia clave con el ejemplo: allá bind() se llamaba una sola vez en
Main y el programa se cerraba. Acá bind() se sigue llamando una vez por
cliente (accept() es bloqueante y atiende de a uno), pero quien decide
cuándo volver a llamar bind() es el loop de atm/main.py, que después de
cerrar la sesión de un cliente vuelve a invocar bind() para aceptar al
siguiente. El servidor completo nunca se apaga solo.
"""

from typing import List

from atm.server.session import Session
from atm.server.socket_process import SocketProcess


class Server(SocketProcess):

    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.session = None

    def bind(self) -> bool:
        try:
            client_socket, address = self.server_socket.accept()
            print(f"Cliente conectado desde {address}")
            self.session = Session(client_socket)
            return True
        except OSError as e:
            print(f"Error aceptando conexión: {e}")
            return False

    def listen(self) -> List[object]:
        data_list: List[object] = []
        next_ = True
        flag = 1
        while next_:
            data = self.session.read()
            if data is None:
                next_ = False
                break
            if isinstance(data, int) and not isinstance(data, bool):
                flag = data
            else:
                flag = 1
            next_ = flag != 0
            if next_:
                data_list.append(data)
        return data_list

    def response(self, data: List[object]) -> bool:
        for d in data:
            self.session.write(d)
        return True

    def close(self) -> bool:
        successful = self.session.close()
        self.session = None
        return successful
