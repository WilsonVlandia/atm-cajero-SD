from abc import ABC, abstractmethod
from typing import Optional, Tuple


class ICajeroServidor(ABC):

    @abstractmethod
    def depositar(self, numero_cuenta: str, clave: str, monto: float) -> Tuple[bool, str, Optional[float]]:
        raise NotImplementedError

    @abstractmethod
    def retirar(self, numero_cuenta: str, clave: str, monto: float) -> Tuple[bool, str, Optional[float]]:
        raise NotImplementedError

    @abstractmethod
    def consultar(self, numero_cuenta: str, clave: str) -> Tuple[bool, str, Optional[float]]:
        raise NotImplementedError
