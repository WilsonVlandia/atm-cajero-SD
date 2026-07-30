// Equivalente a atm/client/client.py.
//
// Misma idea de Listen(): lee objetos hasta encontrar el "flag" 0, que
// actúa de terminador y no se agrega a la lista devuelta. Si el socket se
// cae (Read() devuelve error) cortamos el loop en vez de quedar dando
// vueltas.
package client

import "net"

type Client struct {
	socket  net.Conn
	session *Session
}

func NewClient(socket net.Conn) *Client {
	return &Client{socket: socket}
}

func (c *Client) Connect() bool {
	c.session = NewSession(c.socket)
	return true
}

func (c *Client) Listen() []interface{} {
	var lista []interface{}
	for {
		dato, err := c.session.Read()
		if err != nil {
			break
		}
		// El marcador de fin de transmisión llega como float64(0): json
		// decodifica todo número, en una interface{}, como float64.
		if numero, ok := dato.(float64); ok && numero == 0 {
			break
		}
		lista = append(lista, dato)
	}
	return lista
}

func (c *Client) Response(data []interface{}) bool {
	for _, d := range data {
		c.session.Write(d)
	}
	return true
}

func (c *Client) Close() bool {
	exitoso := c.session.Close()
	c.session = nil
	return exitoso
}
