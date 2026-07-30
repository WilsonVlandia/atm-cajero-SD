"""
Equivalente a lenin.client.Client del profesor.

Misma idea de listen(): lee objetos hasta encontrar el "flag" 0, que
actúa de terminador y no se agrega a la lista. A diferencia del Java
original, si el socket se cae (read() devuelve None) cortamos el loop
en vez de quedar dando vueltas, porque en Python no queda otra forma
de detectar "no hay más datos" sin ese chequeo.
"""

from typing import List

from atm.client.session import Session
from atm.client.socket_process import SocketProcess


class Client(SocketProcess):

    def __init__(self, sock):
        self.socket = sock
        self.session = None

    def connect(self) -> bool:
        try:
            self.session = Session(self.socket)
            return True
        except Exception as e:
            print(f"Error conectando: {e}")
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
