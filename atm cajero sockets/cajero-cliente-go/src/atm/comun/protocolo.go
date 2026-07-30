// Contrato de mensajes que viajan por el socket entre el cajero (cliente)
// y el banco (servidor). Existe también, campo por campo, en el
// protocolo.py de cajero-servidor y cajero-cliente: son proyectos
// independientes que solo se ponen de acuerdo en este "contrato" (mismas
// claves JSON: operacion, numero_cuenta, clave, monto / exitoso, mensaje,
// numero_cuenta, saldo).
package comun

const (
	OpDepositar = "DEPOSITAR"
	OpRetirar   = "RETIRAR"
	OpConsultar = "CONSULTAR"
	OpSalir     = "SALIR"
)

type Peticion struct {
	Operacion    string   `json:"operacion"`
	NumeroCuenta string   `json:"numero_cuenta"`
	Clave        string   `json:"clave"`
	Monto        *float64 `json:"monto"`
}

type Respuesta struct {
	Exitoso      bool     `json:"exitoso"`
	Mensaje      string   `json:"mensaje"`
	NumeroCuenta string   `json:"numero_cuenta"`
	Saldo        *float64 `json:"saldo"`
}

func CrearPeticion(operacion, numeroCuenta, clave string, monto *float64) Peticion {
	return Peticion{
		Operacion:    operacion,
		NumeroCuenta: numeroCuenta,
		Clave:        clave,
		Monto:        monto,
	}
}
