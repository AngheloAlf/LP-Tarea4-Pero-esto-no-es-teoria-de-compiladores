import sys, re
#print sys.argv[1:]

NUMBERLINE = 0
LINEAPROCESADA = ""
PROC = False

def getCommandName():
	if sys.argv[1:]:
		nombre = " ".join(sys.argv[1:])
		return nombre
	else:
		return "alf.alf"


def SintaxError(mensaje = "Error desconocido"):
	print " -- ERROR de sintaxis. -- \nLinea:",NUMBERLINE, "\n"+LINEAPROCESADA
	print mensaje
	exit(0)
	return

def llamadoProcValido(linea): #terminar
	return True

def creacionVariableValido(linea):
	if re.search("^PARAM[0-9]+$", linea):
		SintaxError("Uso de nombre reservado para creacion de variable")
	if len(re.split("[^a-zA-Z]*", linea))>1:
		SintaxError("Uso de caracteres no permitidos para creacion de variable")
	return

def nombreValorValido(linea):
	if lineaVacia(linea):
		SintaxError("No hay valor para asignar a la variable")
	if len(re.split("^TRUE$", linea)) == 2:
		return "True"
	elif len(re.split("^FALSE$", linea)) == 2:
		return "False"
	elif len(re.split("[[\-0-9]*|[0-9]*]", linea)) == 2:
		return linea
	elif len(re.split("[^a-zA-Z]*", linea)) == 1:
		return linea
	else:
		SintaxError("Asignacion de variable invalida")
	return linea

def revisarCreacionVariable(linea):
	return re.search('^VAR\((.*)\)(.*)\s+<=\s+(.*)$', linea) or re.search('^(.*)\s+=>\s+VAR\((.*)\)$', linea)

def lineaVacia(linea):
	if re.search("^[\s\t]*$", linea):
		return True
	return False

def revisarReasignacionVariable(linea):
	if re.search("VAR", linea): return False
	return re.search('^(.*)<=(.*)$', linea) or re.search('^(.*)=>(.*)$', linea)

def eliminarEspacios(linea):
	return re.sub("[\s\t]+", "", linea)

def asignacionAsignosa(variable, valor, crearVar):
	if crearVar:
		creacionVariableValido(variable)
	else:
		pass
	valor = nombreValorValido(valor)
	param = re.split("PARAM", valor)
	if len(param)>1:
		if PROC:
			valor = "params["+param[1]+"]"
		else:
			SintaxError("Uso de la palabra reservada PARAM fuera de una funcion")
	variable = eliminarEspacios(variable)
	valor = eliminarEspacios(valor)
	return variable+" = "+valor

def generarAsignacion(linea, crearVar):
	if lineaVacia(linea): return ""
	asignacionIzq = re.split('<=', linea)
	asignacionDer = re.split('=>', linea)
	if len(asignacionIzq)>1:
		if crearVar: variable = re.split("VAR\(\s*(.*)\)", asignacionIzq[0])[1]
		else: variable = asignacionIzq[0]
		valor = asignacionIzq[1]
	if len(asignacionDer)>1:
		if crearVar: variable = re.split("VAR\(\s*(.*)\)", asignacionDer[1])[1]
		else: variable = asignacionDer[1]
		valor =  asignacionDer[0]
	return asignacionAsignosa(variable, valor, crearVar)

def revisarProcInicio(linea, PROC):
	nombre = re.sub("\)", "", linea)
	nombre = re.split("\$\^PROC\(", nombre)
	if PROC and re.search("\$\^PROC", linea): SintaxError("Funcion dentro de funcion")
	if PROC: return PROC, None
	if re.search("\$\^PROC", linea): return True, nombre[1]
	return False, None

def revisarProcFin(linea, PROC):
	if not PROC and re.search("\^\$", linea): SintaxError()
	if re.search("\^\$", linea): return False
	if PROC: return PROC
	return False

def revisarReturn(linea): #terminar //se refiere al return de las funciones
	pass

def escribirArchivo(nombreArchivo, datosNuevos):
	escribirData = open(nombreArchivo+".py", "w")
	for i in datosNuevos:
		escribirData.write(i)
	return 

nombreArchivo = getCommandName()
datosNuevos = list()
datosNuevos.append("from stdlib import *\n\n")

archivo = open(nombreArchivo)
for i in archivo:
	NUMBERLINE += 1
	LINEAPROCESADA = i
	i = i.strip()
	PROC, nombreProc = revisarProcInicio(i, PROC)
	PROC = revisarProcFin(i, PROC)
	if PROC:
		if nombreProc:
			datosNuevos.append("def "+nombreProc+"(*params):")
		else:
			datosNuevos.append("\t")
			if revisarCreacionVariable(i):
				datosNuevos.append(generarAsignacion(i, True))
			elif revisarReasignacionVariable(i):
				datosNuevos.append(generarAsignacion(i, False))
	else:
		if revisarCreacionVariable(i):
			datosNuevos.append(generarAsignacion(i, True))

	datosNuevos.append("\n")

for i in datosNuevos:
	print i,

escribirArchivo(nombreArchivo, datosNuevos)
