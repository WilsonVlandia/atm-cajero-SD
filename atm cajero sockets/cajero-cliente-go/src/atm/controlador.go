// Equivalente a atm/controlador.py: se inyecta cualquier implementación
// de ICajeroServidor (antes podría ser una local, ahora es el
// CajeroServidorProxy que habla con el banco por sockets). Al controlador
// no le importa.
package main

type CajeroControlador struct {
	servidor ICajeroServidor
}

func NewCajeroControlador(servidor ICajeroServidor) *CajeroControlador {
	return &CajeroControlador{servidor: servidor}
}

func (c *CajeroControlador) Depositar(numeroCuenta, clave string, monto float64) (bool, string, *float64) {
	return c.servidor.Depositar(numeroCuenta, clave, monto)
}

func (c *CajeroControlador) Retirar(numeroCuenta, clave string, monto float64) (bool, string, *float64) {
	return c.servidor.Retirar(numeroCuenta, clave, monto)
}

func (c *CajeroControlador) Consultar(numeroCuenta, clave string) (bool, string, *float64) {
	return c.servidor.Consultar(numeroCuenta, clave)
}
