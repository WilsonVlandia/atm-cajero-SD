// Equivalente a atm/python_client_socket/python_client_socket.py (que a su
// vez replica JavaClientSocket del profesor): arma el socket TCP y lo
// conecta a host:puerto usando net.Dial. Get() devuelve la conexión ya
// establecida, o nil si falló.
package goclientsocket

import (
	"fmt"
	"net"
	"strconv"
)

type GoClientSocket struct {
	Host string
	Port int
}

func NewGoClientSocket(host string, port int) *GoClientSocket {
	return &GoClientSocket{Host: host, Port: port}
}

func (g *GoClientSocket) Get() net.Conn {
	direccion := net.JoinHostPort(g.Host, strconv.Itoa(g.Port))
	conn, err := net.Dial("tcp", direccion)
	if err != nil {
		fmt.Printf("Error creando el socket del cliente: %v\n", err)
		return nil
	}
	return conn
}
