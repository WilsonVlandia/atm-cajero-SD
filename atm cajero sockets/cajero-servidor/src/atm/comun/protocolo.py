"""
Contrato de mensajes que viajan por el socket entre el cajero (cliente)
y el banco (servidor). Este archivo existe también, palabra por palabra,
en cajero-cliente/src/atm/comun/protocolo.py: son dos proyectos
independientes (como clientsocket/ y socketserver/ del profesor), así
que no comparten import, solo se ponen de acuerdo en este "contrato".
"""

OP_DEPOSITAR = "DEPOSITAR"
OP_RETIRAR = "RETIRAR"
OP_CONSULTAR = "CONSULTAR"
OP_SALIR = "SALIR"


def crear_peticion(operacion: str, numero_cuenta: str, clave: str, monto: float = None) -> dict:
    return {
        "operacion": operacion,
        "numero_cuenta": numero_cuenta,
        "clave": clave,
        "monto": monto,
    }


def crear_respuesta(exitoso: bool, mensaje: str, numero_cuenta: str, saldo) -> dict:
    return {
        "exitoso": exitoso,
        "mensaje": mensaje,
        "numero_cuenta": numero_cuenta,
        "saldo": saldo,
    }
