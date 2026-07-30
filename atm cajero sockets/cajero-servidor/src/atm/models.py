from dataclasses import dataclass


@dataclass
class Cuenta:
    """Representa una cuenta bancaria."""
    numero_cuenta: str
    clave: str
    saldo: float
