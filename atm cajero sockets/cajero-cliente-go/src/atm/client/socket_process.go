// Equivalente a atm/client/socket_process.py: en Java es una interface, en
// Python una ABC; en Go usamos directamente una interface del lenguaje.
package client

type SocketProcess interface {
	Connect() bool
	Listen() []interface{}
	Response(data []interface{}) bool
	Close() bool
}
