import sys

class errorAux:
	NUMBERLINE = 0
	LINEAPROCESADA = ""

def IOerror(mensaje = "Error desconocido"):
	print " -- I/O ERROR -- \n"+mensaje
	exit(0)
	return

def sintaxError(mensaje = "Error desconocido"):
	print " -- ERROR de sintaxis. -- \nLinea:",errorAux.NUMBERLINE, "\n"+errorAux.LINEAPROCESADA+"\n"+mensaje
	exit(0)
	return

def getCommandName():
	if sys.argv[1:]:
		return " ".join(sys.argv[1:])
	else:
		IOerror("No se ingreso un archivo para traducir.")

def borrarNulos(lista):
	return [x for x in lista if x]

def escribirArchivo(nombreArchivo, datosNuevos):
	escribirData = open(nombreArchivo+".py", "w")
	for i in datosNuevos:
		escribirData.write(i)
	return
