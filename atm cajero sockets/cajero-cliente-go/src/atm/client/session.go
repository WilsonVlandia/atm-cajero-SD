// Equivalente a atm/client/session.py. Java usa
// ObjectOutputStream/ObjectInputStream (writeObject/readObject); ni Python
// ni Go tienen eso "de fábrica" para sockets, así que armamos el mismo
// framing manual sobre la conexión TCP:
//
//	[ 4 bytes big-endian: cuántos bytes vienen ][ N bytes: el JSON en sí ]
//
// para que Read() sepa exactamente cuántos bytes leer sin adivinar dónde
// termina un mensaje y empieza el siguiente.
package client

import (
	"encoding/binary"
	"encoding/json"
	"net"
)

type Session struct {
	conn net.Conn
}

func NewSession(conn net.Conn) *Session {
	return &Session{conn: conn}
}

// recvExact lee exactamente n bytes, haciendo loop si hace falta: recv()
// no siempre entrega todos los bytes pedidos de una sola vez.
func (s *Session) recvExact(n int) ([]byte, error) {
	buf := make([]byte, n)
	leidos := 0
	for leidos < n {
		m, err := s.conn.Read(buf[leidos:])
		if err != nil {
			return nil, err
		}
		leidos += m
	}
	return buf, nil
}

func (s *Session) Read() (interface{}, error) {
	header, err := s.recvExact(4)
	if err != nil {
		return nil, err
	}
	longitud := binary.BigEndian.Uint32(header)
	payload, err := s.recvExact(int(longitud))
	if err != nil {
		return nil, err
	}
	var dato interface{}
	if err := json.Unmarshal(payload, &dato); err != nil {
		return nil, err
	}
	return dato, nil
}

func (s *Session) Write(dato interface{}) bool {
	payload, err := json.Marshal(dato)
	if err != nil {
		return false
	}
	header := make([]byte, 4)
	binary.BigEndian.PutUint32(header, uint32(len(payload)))
	if _, err := s.conn.Write(append(header, payload...)); err != nil {
		return false
	}
	return true
}

func (s *Session) Close() bool {
	return s.conn.Close() == nil
}
