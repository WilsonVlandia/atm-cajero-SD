import threading
from typing import Dict, Optional, Tuple

from atm.interfaces import ICajeroServidor
from atm.models import Cuenta


class CajeroServidor(ICajeroServidor):

    def __init__(self):
        self._lock = threading.Lock()
        # "Base de datos" quemada de cuentas de prueba, en memoria.
        self._cuentas: Dict[str, Cuenta] = {
            "1001": Cuenta("1001", "1234", 500000.0),
            "1002": Cuenta("1002", "4321", 150000.0),
            "1003": Cuenta("1003", "0000", 0.0),
        }

    def depositar(self, numero_cuenta: str, clave: str, monto: float) -> Tuple[bool, str, Optional[float]]:
        with self._lock:
            cuenta, error = self._autenticar(numero_cuenta, clave)
            if error:
                return False, error, None

            if monto <= 0:
                return False, "El monto ingresado no es válido (debe ser mayor a cero).", cuenta.saldo

            cuenta.saldo += monto
            return True, "Depósito realizado con éxito.", cuenta.saldo

    def retirar(self, numero_cuenta: str, clave: str, monto: float) -> Tuple[bool, str, Optional[float]]:
        with self._lock:
            cuenta, error = self._autenticar(numero_cuenta, clave)
            if error:
                return False, error, None

            if monto <= 0:
                return False, "El monto ingresado no es válido (debe ser mayor a cero).", cuenta.saldo

            if monto > cuenta.saldo:
                return False, "Saldo insuficiente para realizar el retiro.", cuenta.saldo

            cuenta.saldo -= monto
            return True, "Retiro realizado con éxito.", cuenta.saldo

    def consultar(self, numero_cuenta: str, clave: str) -> Tuple[bool, str, Optional[float]]:
        with self._lock:
            cuenta, error = self._autenticar(numero_cuenta, clave)
            if error:
                return False, error, None

            return True, "Consulta realizada con éxito.", cuenta.saldo

    def _autenticar(self, numero_cuenta: str, clave: str) -> Tuple[Optional[Cuenta], Optional[str]]:
        """Retorna (cuenta, None) si todo está bien, o (None, mensaje_error) si no."""
        cuenta = self._cuentas.get(numero_cuenta)
        if cuenta is None:
            return None, "La cuenta ingresada no existe."
        if cuenta.clave != clave:
            return None, "La clave ingresada es incorrecta."
        return cuenta, None
