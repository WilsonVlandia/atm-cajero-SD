// Equivalente a atm/interfaces.py: ICajeroServidor. En Go la interfaz es
// del lenguaje directamente, sin necesidad de ABC.
package main

type ICajeroServidor interface {
	Depositar(numeroCuenta, clave string, monto float64) (bool, string, *float64)
	Retirar(numeroCuenta, clave string, monto float64) (bool, string, *float64)
	Consultar(numeroCuenta, clave string) (bool, string, *float64)
}
