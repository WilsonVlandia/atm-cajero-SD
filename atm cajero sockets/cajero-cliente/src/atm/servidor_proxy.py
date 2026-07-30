"""
CajeroServidorProxy: implementa ICajeroServidor igual que antes lo hacía
CajeroServidor local, pero en vez de tocar un diccionario en memoria,
arma una petición, la manda por el socket (client.response) y espera
la respuesta (client.listen()). Es el "traductor" entre la interfaz de
negocio del cajero y el protocolo de sockets del profesor.
"""

from typing import Optional, Tuple

from atm.client.socket_process import SocketProcess
from atm.comun.protocolo import (
    OP_CONSULTAR,
    OP_DEPOSITAR,
    OP_RETIRAR,
    OP_SALIR,
    crear_peticion,
)
from atm.interfaces import ICajeroServidor


class CajeroServidorProxy(ICajeroServidor):

    def __init__(self, client: SocketProcess):
        self._client = client

    def depositar(self, numero_cuenta: str, clave: str, monto: float) -> Tuple[bool, str, Optional[float]]:
        return self._enviar(crear_peticion(OP_DEPOSITAR, numero_cuenta, clave, monto))

    def retirar(self, numero_cuenta: str, clave: str, monto: float) -> Tuple[bool, str, Optional[float]]:
        return self._enviar(crear_peticion(OP_RETIRAR, numero_cuenta, clave, monto))

    def consultar(self, numero_cuenta: str, clave: str) -> Tuple[bool, str, Optional[float]]:
        return self._enviar(crear_peticion(OP_CONSULTAR, numero_cuenta, clave))

    def cerrar_sesion(self) -> None:
        """Avisa al servidor que este cliente ya terminó, para que vuelva
        a quedar disponible y pueda atender al siguiente."""
        self._client.response([crear_peticion(OP_SALIR, "", ""), 0])

    def _enviar(self, peticion: dict) -> Tuple[bool, str, Optional[float]]:
        self._client.response([peticion, 0])
        respuestas = self._client.listen()
        if not respuestas:
            return False, "Se perdió la conexión con el servidor.", None
        respuesta = respuestas[0]
        return respuesta["exitoso"], respuesta["mensaje"], respuesta["saldo"]
