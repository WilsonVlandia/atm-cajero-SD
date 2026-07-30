"""
Equivalente a lenin.Main del profesor (socketserver), pero el programa
NO se apaga después de atender un cliente: se queda prendido en un
loop infinito, atendiendo un cliente a la vez (accept() es bloqueante,
así que mientras un cliente está conectado nadie más entra a la cola,
pero apenas se desconecta, el loop vuelve a bind() y recibe al
siguiente).
"""

from atm.cajero_servidor import CajeroServidor
from atm.comun.protocolo import OP_CONSULTAR, OP_DEPOSITAR, OP_RETIRAR, OP_SALIR, crear_respuesta
from atm.python_server_socket.python_server_socket import PythonServerSocket
from atm.server.server import Server

PUERTO = 1802
BACKLOG = 100


def procesar_peticion(peticion: dict, cajero: CajeroServidor) -> dict:
    operacion = peticion.get("operacion")
    numero_cuenta = peticion.get("numero_cuenta")
    clave = peticion.get("clave")
    monto = peticion.get("monto")

    if operacion == OP_DEPOSITAR:
        exitoso, mensaje, saldo = cajero.depositar(numero_cuenta, clave, monto)
    elif operacion == OP_RETIRAR:
        exitoso, mensaje, saldo = cajero.retirar(numero_cuenta, clave, monto)
    elif operacion == OP_CONSULTAR:
        exitoso, mensaje, saldo = cajero.consultar(numero_cuenta, clave)
    else:
        exitoso, mensaje, saldo = False, f"Operación desconocida: {operacion}", None

    return crear_respuesta(exitoso, mensaje, numero_cuenta, saldo)


def atender_cliente(server: Server, cajero: CajeroServidor) -> None:
    """Mientras el mismo cliente siga conectado, procesa todas las
    operaciones que pida (depositar/retirar/consultar), una por una,
    hasta que mande SALIR o se caiga la conexión."""
    while True:
        peticiones = server.listen()
        if not peticiones:
            print("Cliente desconectado sin avisar (SALIR).")
            return

        peticion = peticiones[0]
        if peticion.get("operacion") == OP_SALIR:
            print("Cliente pidió salir.")
            return

        respuesta = procesar_peticion(peticion, cajero)
        server.response([respuesta, 0])


def main():
    print("Cajero Automático - Servidor (socket)")

    python_server_socket = PythonServerSocket(PUERTO, BACKLOG)
    server_socket = python_server_socket.get()
    if server_socket is None:
        print("No se pudo abrir el servidor")
        return

    server = Server(server_socket)
    cajero = CajeroServidor()

    print(f"Servidor escuchando en el puerto {PUERTO}. Esperando clientes...")

    try:
        while True:
            if not server.bind():
                continue

            try:
                atender_cliente(server, cajero)
            finally:
                server.close()
                print("Sesión cerrada. Esperando siguiente cliente...\n")
    except KeyboardInterrupt:
        print("\nServidor detenido manualmente.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
