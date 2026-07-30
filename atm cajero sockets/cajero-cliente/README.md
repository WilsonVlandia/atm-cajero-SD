# Cajero ATM - Cliente (sockets)

Cajero físico / terminal. Se conecta una vez al servidor y, mientras el
usuario no elija "Salir", mantiene la misma conexión para todas las
operaciones del menú (depositar, retirar, consultar).

Estructura calcada de `clientsocket` (el ejemplo del profesor: paquete
`lenin`, subpaquetes `client/` y `java_client_socket/`), pero en Python:

```
cajero-cliente/
└── src/
    └── atm/
        ├── main.py                     # equivalente a lenin.Main: conecta y corre el menú
        ├── interfaces.py               # ICajeroServidor (mismo contrato que el servidor)
        ├── controlador.py              # CajeroControlador: delega en ICajeroServidor, sin lógica propia
        ├── servidor_proxy.py           # CajeroServidorProxy(ICajeroServidor): traduce llamadas -> peticiones por socket
        ├── client/                     # equivalente a lenin.client
        │   ├── socket_process.py       #   SocketProcess (connect/listen/response/close)
        │   ├── session.py              #   Session (lee/escribe objetos framed con JSON)
        │   └── client.py               #   Client(SocketProcess)
        ├── python_client_socket/       # equivalente a lenin.java_client_socket
        │   └── python_client_socket.py #   PythonClientSocket: crea y conecta el socket
        └── comun/
            └── protocolo.py            # contrato de mensajes (igual, palabra por palabra, al del servidor)
```

## Cómo correrlo

Con el servidor ya prendido (ver `cajero-servidor/README.md`):

```bash
cd cajero-cliente/src
PYTHONPATH=. python3 -m atm.main
```

Se conecta a `127.0.0.1:1802`.

## Cómo encaja con la arquitectura anterior

Antes (`atm cajero/`, sin red), `client.py` inyectaba un `CajeroServidor`
local directo en el `CajeroControlador`. Ahora se inyecta un
`CajeroServidorProxy`, que cumple la misma interfaz `ICajeroServidor`
pero por dentro arma una petición, la manda por el socket
(`client.response([...])`) y espera la respuesta (`client.listen()`).
El `controlador.py` y el menú de `main.py` no cambiaron en su lógica:
no les importa si el servidor está en el mismo proceso o al otro lado
de un socket.
