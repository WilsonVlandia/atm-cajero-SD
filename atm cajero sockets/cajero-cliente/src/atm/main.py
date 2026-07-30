"""
Equivalente a lenin.Main del profesor (clientsocket), adaptado al menú
del cajero. Arma el socket, conecta, inyecta el CajeroServidorProxy en
el CajeroControlador, y de ahí en adelante el menú es igual al de la
versión sin red: no le importa que la implementación de ICajeroServidor
converse por un socket en vez de vivir en el mismo proceso.
"""

from atm.client.client import Client
from atm.controlador import CajeroControlador
from atm.python_client_socket.python_client_socket import PythonClientSocket
from atm.servidor_proxy import CajeroServidorProxy

HOST = "127.0.0.1"
PUERTO = 1802


def mostrar_menu():
    print("\n----------------------------------------")
    print("1. Depositar")
    print("2. Retirar")
    print("3. Consultar saldo")
    print("0. Salir")
    print("----------------------------------------")


def mostrar_resultado(exitoso: bool, mensaje: str, numero_cuenta: str, saldo):
    print()
    if exitoso:
        print(">> " + mensaje)
    else:
        print(">> ERROR: " + mensaje)

    if saldo is not None:
        print(f">> Cuenta: {numero_cuenta} | Saldo actual: ${saldo:.2f}")


def pedir_monto(mensaje: str) -> float:
    return float(input(mensaje).strip())


def main():
    print("Cajero Automático - Cliente (socket)")

    python_client_socket = PythonClientSocket(PUERTO, HOST)
    client_socket = python_client_socket.get()
    if client_socket is None:
        print(f"No se pudo conectar al servidor en {HOST}:{PUERTO}. ¿Está prendido?")
        return

    client = Client(client_socket)
    if not client.connect():
        print("Falló la conexión con el servidor")
        return

    servidor = CajeroServidorProxy(client)
    controlador = CajeroControlador(servidor)

    print("========================================")
    print("   BIENVENIDO AL CAJERO AUTOMÁTICO")
    print("========================================")
    print("Cuentas de prueba: 1001/1234 | 1002/4321 | 1003/0000")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            numero_cuenta = input("Número de cuenta: ").strip()
            try:
                monto = pedir_monto("Monto a depositar: ")
            except ValueError:
                print(">> El monto ingresado no es un número válido.")
                continue
            clave = input("Clave: ").strip()
            exitoso, mensaje, saldo = controlador.depositar(numero_cuenta, clave, monto)
            mostrar_resultado(exitoso, mensaje, numero_cuenta, saldo)

        elif opcion == "2":
            numero_cuenta = input("Número de cuenta: ").strip()
            try:
                monto = pedir_monto("Monto a retirar: ")
            except ValueError:
                print(">> El monto ingresado no es un número válido.")
                continue
            clave = input("Clave: ").strip()
            exitoso, mensaje, saldo = controlador.retirar(numero_cuenta, clave, monto)
            mostrar_resultado(exitoso, mensaje, numero_cuenta, saldo)

        elif opcion == "3":
            numero_cuenta = input("Número de cuenta: ").strip()
            clave = input("Clave: ").strip()
            exitoso, mensaje, saldo = controlador.consultar(numero_cuenta, clave)
            mostrar_resultado(exitoso, mensaje, numero_cuenta, saldo)

        elif opcion == "0":
            servidor.cerrar_sesion()
            client.close()
            print("Gracias por usar el cajero. ¡Hasta pronto!")
            break

        else:
            print(">> Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()
