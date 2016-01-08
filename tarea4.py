import sys, re
#print sys.argv[1:]

NUMBERLINE = 0
LINEAPROCESADA = ""

def getCommandName():
	if sys.argv[1:]:
		nombre = " ".join(sys.argv[1:])
		return nombre
	else:
		return "alf.alf"


def SintaxError(mensaje = ""):
	print " -- ERROR de sintaxis. -- \nLinea:",NUMBERLINE, "\n"+LINEAPROCESADA
	print mensaje
	exit(0)
	return

def llamadoProcValido(linea): #terminar
	return True

def nombreVariableValido(linea):
	if re.search("PARAM[0-9]+", linea):
		return
	if len(re.split("^[a-zA-Z]$", linea))>1:
		SintaxError()
	return

def nombreValorValido(linea):
	numeros = re.split("[[\-0-9]*|[0-9]*]", linea)
	boolenas = re.split("TRUE|FALSE", linea)
	charateres = re.split("[^a-zA-Z]", linea)
	#print numeros
	#print boolenas
	if (len(numeros)>1 and len(boolenas)>1 and len(charateres)>1) or not llamadoProcValido(linea):
		SintaxError()

def revisarAsignacion(linea):
	return re.search('<=', linea) or re.search('=>', linea)

def lineaVacia(linea):
	if re.search("^[\s\t]*$", linea):
		return True
	return False

def asignacionAsignosa(variable, valor):
	buscando = re.search("VAR", variable)
	c = variable[buscando.span()[1]:]
	variable = re.split("\(\s*(.*)\)", c)
	variable = variable[1]
	variable = re.sub("[\s\t]", "", variable)
	nombreVariableValido(variable)
	#param = re.split("PARAM", variable)
	#if len(param)>1:
	#	variable = "params["+param[1]+"]"
	valor = re.sub("[\s\t]","",valor)
	nombreValorValido(valor)
	param = re.split("PARAM", valor)
	if len(param)>1:
		valor = "params["+param[1]+"]"
	return variable+" = "+valor

def generarAsignacion(linea):
	if lineaVacia(linea):
		return ""
	asignacionIzq = re.split('<=', linea)
	asignacionDer = re.split('=>', linea)

	if len(asignacionIzq)>1:
		return asignacionAsignosa(asignacionIzq[0], asignacionIzq[1])

	if len(asignacionDer)>1:
		return asignacionAsignosa(asignacionDer[1], asignacionDer[0])

	return None

def revisarProcInicio(linea, proc):
	nombre = re.sub("\)", "", linea)
	nombre = re.split("\$\^PROC\(", nombre)
	if proc and re.search("\$\^PROC", linea): SintaxError("Funcion dentro de funcion")
	if proc: return proc, None
	if re.search("\$\^PROC", linea): return True, nombre[1]
	return False, None

def revisarProcFin(linea, proc):
	if not proc and re.search("\^\$", linea): SintaxError()
	if re.search("\^\$", linea): return False
	if proc: return proc
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
proc = False
inFuncData = list()

archivo = open(nombreArchivo)
for i in archivo:
	NUMBERLINE += 1
	LINEAPROCESADA = i
	i = i.strip()
	proc, nombreProc = revisarProcInicio(i, proc)
	proc = revisarProcFin(i, proc)
	if proc:
		if nombreProc:
			datosNuevos.append("def "+nombreProc+"(*params):")
		else:
			datosNuevos.append("\t")
			datosNuevos.append(generarAsignacion(i))
	else:
		inFuncData = list()
		
		if revisarAsignacion(i):
			datosNuevos.append(generarAsignacion(i))

	datosNuevos.append("\n")

print datosNuevos

escribirArchivo(nombreArchivo, datosNuevos)