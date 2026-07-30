"""
Equivalente a lenin.client.Session del profesor.

Java usa ObjectOutputStream/ObjectInputStream (writeObject/readObject).
Python no tiene eso "de fábrica" para sockets, así que armamos un framing
simple sobre los file objects del socket (socket.makefile): cada objeto
se serializa a JSON y se antecede por su longitud en 4 bytes (big-endian),
para que read() sepa exactamente cuántos bytes leer sin adivinar dónde
termina un mensaje y empieza el siguiente.
"""

import json
import socket
import struct


class Session:

    def __init__(self, sock: socket.socket):
        self.socket = sock
        try:
            self._wfile = sock.makefile("wb")
            self._rfile = sock.makefile("rb")
        except Exception as e:
            print(f"Error creando la sesión: {e}")
            self._wfile = None
            self._rfile = None
            self.socket = None

    def read(self):
        try:
            header = self._rfile.read(4)
            if not header or len(header) < 4:
                return None
            (longitud,) = struct.unpack("!I", header)
            payload = self._rfile.read(longitud)
            if len(payload) < longitud:
                return None
            return json.loads(payload.decode("utf-8"))
        except (OSError, AttributeError, ValueError, json.JSONDecodeError):
            return None

    def write(self, data) -> bool:
        try:
            payload = json.dumps(data).encode("utf-8")
            self._wfile.write(struct.pack("!I", len(payload)))
            self._wfile.write(payload)
            self._wfile.flush()
            return True
        except (OSError, AttributeError, TypeError, ValueError) as e:
            print(f"Error escribiendo en la sesión: {e}")
            return False

    def close(self) -> bool:
        try:
            if self._wfile:
                self._wfile.close()
            if self._rfile:
                self._rfile.close()
            if self.socket:
                self.socket.close()
            return True
        except OSError as e:
            print(f"Error cerrando la sesión: {e}")
            return False
