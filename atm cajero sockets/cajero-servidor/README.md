# Cajero ATM - Servidor (sockets)

Banco / servidor del cajero. Se queda **prendido en loop**, atendiendo
**un cliente a la vez** (accept() bloqueante) hasta que lo detengas con
Ctrl+C. Cada vez que un cliente termina (opción "Salir" o se cae la
conexión), el servidor vuelve a quedar disponible para el siguiente.

Estructura calcada de `socketserver` (el ejemplo del profesor: paquete
`lenin`, subpaquetes `server/` y `java_server_socket/`), pero en Python:

```
cajero-servidor/
└── src/
    └── atm/
        ├── main.py                     # equivalente a lenin.Main: loop infinito, un cliente a la vez
        ├── models.py                   # Cuenta (numero_cuenta, clave, saldo)
        ├── interfaces.py               # ICajeroServidor (contrato de negocio)
        ├── cajero_servidor.py          # CajeroServidor: lógica + "BD" en memoria
        ├── server/                     # equivalente a lenin.server
        │   ├── socket_process.py       #   SocketProcess (bind/listen/response/close)
        │   ├── session.py              #   Session (lee/escribe objetos framed con JSON)
        │   └── server.py               #   Server(SocketProcess)
        ├── python_server_socket/       # equivalente a lenin.java_server_socket
        │   └── python_server_socket.py #   PythonServerSocket: crea el socket que escucha
        └── comun/
            └── protocolo.py            # contrato de mensajes (operaciones + forma del dict)
```

## Cómo correrlo

```bash
cd cajero-servidor/src
PYTHONPATH=. python3 -m atm.main
```

Escucha en `0.0.0.0:1802`. Para detenerlo: `Ctrl+C`.

## Cuentas de prueba (quemadas en memoria)

| Cuenta | Clave | Saldo inicial |
|--------|-------|---------------|
| 1001   | 1234  | 500000        |
| 1002   | 4321  | 150000        |
| 1003   | 0000  | 0             |

## Diferencia clave con el ejemplo del profesor

En el ejemplo, `Main` llamaba `bind()` una sola vez, hacía un
`listen()`/`response()` y cerraba todo. Acá `atm/main.py` pone ese
mismo ciclo (`bind → atender → close`) dentro de un `while True`, así
que el proceso nunca se apaga solo: sigue escuchando para el próximo
cliente.
