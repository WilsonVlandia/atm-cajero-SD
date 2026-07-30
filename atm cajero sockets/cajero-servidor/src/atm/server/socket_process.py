"""
Equivalente a lenin.server.SocketProcess del profesor: bind() en vez de
connect(), porque del lado servidor la operación es aceptar, no conectar.
"""

from abc import ABC, abstractmethod
from typing import List


class SocketProcess(ABC):

    @abstractmethod
    def bind(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def listen(self) -> List[object]:
        raise NotImplementedError

    @abstractmethod
    def response(self, data: List[object]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> bool:
        raise NotImplementedError
