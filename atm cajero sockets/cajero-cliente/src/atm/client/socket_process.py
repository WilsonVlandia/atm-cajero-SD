"""
Equivalente a lenin.client.SocketProcess del profesor:
en Java es una interface, en Python usamos ABC.
"""

from abc import ABC, abstractmethod
from typing import List


class SocketProcess(ABC):

    @abstractmethod
    def connect(self) -> bool:
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
