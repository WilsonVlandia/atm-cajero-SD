from typing import Optional, Tuple

from atm.interfaces import ICajeroServidor


class CajeroControlador:

    def __init__(self, servidor: ICajeroServidor):
        # Se inyecta una instancia que cumpla la interfaz ICajeroServidor.
        # Antes era un CajeroServidor local; ahora es un CajeroServidorProxy
        # que habla con el banco por sockets. Al controlador no le importa.
        self._servidor = servidor

    def depositar(self, numero_cuenta: str, clave: str, monto: float) -> Tuple[bool, str, Optional[float]]:
        return self._servidor.depositar(numero_cuenta, clave, monto)

    def retirar(self, numero_cuenta: str, clave: str, monto: float) -> Tuple[bool, str, Optional[float]]:
        return self._servidor.retirar(numero_cuenta, clave, monto)

    def consultar(self, numero_cuenta: str, clave: str) -> Tuple[bool, str, Optional[float]]:
        return self._servidor.consultar(numero_cuenta, clave)
