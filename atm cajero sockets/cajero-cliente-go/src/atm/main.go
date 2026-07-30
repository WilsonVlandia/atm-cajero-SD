// Equivalente a atm/main.py: arma el socket, conecta, inyecta el
// CajeroServidorProxy en el CajeroControlador y corre el mismo menú que
// la versión Python — no le importa que ICajeroServidor converse por un
// socket en vez de vivir en el mismo proceso. Habla con el mismo servidor
// (Python, en cajero-servidor): mismo host, mismo puerto y mismo
// protocolo JSON, así que da igual qué cliente se conecte.
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	"cajeroclientego/src/atm/client"
	goclientsocket "cajeroclientego/src/atm/go_client_socket"
)

const (
	host   = "127.0.0.1"
	puerto = 1802
)

var lector = bufio.NewReader(os.Stdin)

func leerLinea(mensaje string) string {
	fmt.Print(mensaje)
	linea, _ := lector.ReadString('\n')
	return strings.TrimSpace(linea)
}

func mostrarMenu() {
	fmt.Println("\n----------------------------------------")
	fmt.Println("1. Depositar")
	fmt.Println("2. Retirar")
	fmt.Println("3. Consultar saldo")
	fmt.Println("0. Salir")
	fmt.Println("----------------------------------------")
}

func mostrarResultado(exitoso bool, mensaje, numeroCuenta string, saldo *float64) {
	fmt.Println()
	if exitoso {
		fmt.Println(">> " + mensaje)
	} else {
		fmt.Println(">> ERROR: " + mensaje)
	}
	if saldo != nil {
		fmt.Printf(">> Cuenta: %s | Saldo actual: $%.2f\n", numeroCuenta, *saldo)
	}
}

func pedirMonto(mensaje string) (float64, error) {
	return strconv.ParseFloat(leerLinea(mensaje), 64)
}

func main() {
	fmt.Println("Cajero Automático - Cliente (socket, Go)")

	socketCliente := goclientsocket.NewGoClientSocket(host, puerto)
	conexion := socketCliente.Get()
	if conexion == nil {
		fmt.Printf("No se pudo conectar al servidor en %s:%d. ¿Está prendido?\n", host, puerto)
		return
	}

	atmCliente := client.NewClient(conexion)
	if !atmCliente.Connect() {
		fmt.Println("Falló la conexión con el servidor")
		return
	}

	servidor := NewCajeroServidorProxy(atmCliente)
	controlador := NewCajeroControlador(servidor)

	fmt.Println("========================================")
	fmt.Println("   BIENVENIDO AL CAJERO AUTOMÁTICO")
	fmt.Println("========================================")
	fmt.Println("Cuentas de prueba: 1001/1234 | 1002/4321 | 1003/0000")

	for {
		mostrarMenu()
		opcion := leerLinea("Seleccione una opción: ")

		switch opcion {
		case "1":
			numeroCuenta := leerLinea("Número de cuenta: ")
			monto, err := pedirMonto("Monto a depositar: ")
			if err != nil {
				fmt.Println(">> El monto ingresado no es un número válido.")
				continue
			}
			clave := leerLinea("Clave: ")
			exitoso, mensaje, saldo := controlador.Depositar(numeroCuenta, clave, monto)
			mostrarResultado(exitoso, mensaje, numeroCuenta, saldo)

		case "2":
			numeroCuenta := leerLinea("Número de cuenta: ")
			monto, err := pedirMonto("Monto a retirar: ")
			if err != nil {
				fmt.Println(">> El monto ingresado no es un número válido.")
				continue
			}
			clave := leerLinea("Clave: ")
			exitoso, mensaje, saldo := controlador.Retirar(numeroCuenta, clave, monto)
			mostrarResultado(exitoso, mensaje, numeroCuenta, saldo)

		case "3":
			numeroCuenta := leerLinea("Número de cuenta: ")
			clave := leerLinea("Clave: ")
			exitoso, mensaje, saldo := controlador.Consultar(numeroCuenta, clave)
			mostrarResultado(exitoso, mensaje, numeroCuenta, saldo)

		case "0":
			servidor.CerrarSesion()
			atmCliente.Close()
			fmt.Println("Gracias por usar el cajero. ¡Hasta pronto!")
			return

		default:
			fmt.Println(">> Opción inválida, intente de nuevo.")
		}
	}
}
