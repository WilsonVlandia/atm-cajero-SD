// Equivalente a atm/servidor_proxy.py: CajeroServidorProxy implementa
// ICajeroServidor igual que antes lo haría un CajeroServidor local, pero
// en vez de tocar datos en memoria, arma una petición, la manda por el
// socket (cliente.Response) y espera la respuesta (cliente.Listen()). Es
// el "traductor" entre la interfaz de negocio del cajero y el protocolo
// de sockets del profesor.
package main

import (
	"encoding/json"

	"cajeroclientego/src/atm/client"
	"cajeroclientego/src/atm/comun"
)

type CajeroServidorProxy struct {
	cliente client.SocketProcess
}

func NewCajeroServidorProxy(cliente client.SocketProcess) *CajeroServidorProxy {
	return &CajeroServidorProxy{cliente: cliente}
}

func (p *CajeroServidorProxy) Depositar(numeroCuenta, clave string, monto float64) (bool, string, *float64) {
	return p.enviar(comun.CrearPeticion(comun.OpDepositar, numeroCuenta, clave, &monto))
}

func (p *CajeroServidorProxy) Retirar(numeroCuenta, clave string, monto float64) (bool, string, *float64) {
	return p.enviar(comun.CrearPeticion(comun.OpRetirar, numeroCuenta, clave, &monto))
}

func (p *CajeroServidorProxy) Consultar(numeroCuenta, clave string) (bool, string, *float64) {
	return p.enviar(comun.CrearPeticion(comun.OpConsultar, numeroCuenta, clave, nil))
}

// CerrarSesion avisa al servidor que este cliente ya terminó, para que
// vuelva a quedar disponible y pueda atender al siguiente.
func (p *CajeroServidorProxy) CerrarSesion() {
	p.cliente.Response([]interface{}{comun.CrearPeticion(comun.OpSalir, "", "", nil), 0})
}

func (p *CajeroServidorProxy) enviar(peticion comun.Peticion) (bool, string, *float64) {
	p.cliente.Response([]interface{}{peticion, 0})
	respuestas := p.cliente.Listen()
	if len(respuestas) == 0 {
		return false, "Se perdió la conexión con el servidor.", nil
	}

	// El servidor responde JSON genérico (map[string]interface{}); re
	// serializamos y deserializamos contra Respuesta para reconstruirlo,
	// en vez de extraer cada campo a mano.
	raw, err := json.Marshal(respuestas[0])
	if err != nil {
		return false, "Error al procesar la respuesta del servidor.", nil
	}
	var respuesta comun.Respuesta
	if err := json.Unmarshal(raw, &respuesta); err != nil {
		return false, "Error al procesar la respuesta del servidor.", nil
	}
	return respuesta.Exitoso, respuesta.Mensaje, respuesta.Saldo
}
