import sys, re

# print sys.argv[1:]

NUMBERLINE = 0
LINEAPROCESADA = ""
PROC = False

def IOerror(mensaje = "Error desconocido"):
	print " -- I/O ERROR -- "
	print mensaje
	exit(0)
	return

def getCommandName():
	if sys.argv[1:]:
		return " ".join(sys.argv[1:])
	else:
		IOerror("No se ingreso un archivo para traducir.")

def sintaxError(mensaje = "Error desconocido"):
	print " -- ERROR de sintaxis. -- \nLinea:",NUMBERLINE, "\n"+LINEAPROCESADA
	print mensaje
	exit(0)
	return

def llamadoProcValido(linea):
	a = re.split("\((.*)\)", linea)
	if not a: return False
	if len(a)>1:
		if re.search("\(|\)", a[1]): sintaxError("Se realizo llamado de funcion dentro de llamado de funcion")
		return True
	return False

def formatearLlamadoProc(linea):
	if re.search("\(\s*\)", linea):
		return "pass"
	a = re.split("\((.*)\)", linea)[1]
	b = re.split("\s", a)
	return b[0]+"("+", ".join(map(nombreValorValido, b[1:]))+")"

def creacionVariableValido(linea):
	if re.search("^PARAM[0-9]+$", linea):
		sintaxError("Uso de nombre reservado para creacion de variable")
	return

def borrarNulos(lista):
	return [x for x in lista if x]

def nombreVariableValido(linea):
	if len(borrarNulos(re.split("\s*", linea))) != 1:
		if len(re.split("[^a-zA-Z]*", linea)) != 1:
			sintaxError("Uso de caracteres no permitidos para una variable")
	return

def nombreValorValido(linea):
	if lineaVacia(linea):
		sintaxError("No hay valor para asignar a la variable")
	elif re.search("^PARAM[0-9]+$", linea):
		return "params["+re.split("PARAM", linea)[1]+"]"
	elif revisarIFELSE(linea):
		return formatearIFELESE(linea)
	elif llamadoProcValido(linea):
		return formatearLlamadoProc(linea)
	elif len(re.split("^TRUE$", linea)) == 2:
		return "True"
	elif len(re.split("^FALSE$", linea)) == 2:
		return "False"
	elif len(re.split("[[\-0-9]*|[0-9]*]", linea)) == 2:
		return eliminarEspacios(linea)
	elif not nombreVariableValido(linea):
		return eliminarEspacios(linea)
	else:
		sintaxError("Asignacion de variable invalida")

def revisarCreacionVariable(linea):
	return re.search('^VAR\((.*)\)(.*)\s+<=\s+(.*)$', linea) or re.search('^(.*)\s+=>\s+VAR\((.*)\)$', linea)

def lineaVacia(linea):
	if re.search("^\s*$", linea):
		return True
	return False

def revisarReasignacionVariable(linea):
	if re.search("VAR", linea): return False
	return re.search('^(.*)<=(.*)$', linea) or re.search('^(.*)=>(.*)$', linea)

def eliminarEspacios(linea):
	return re.sub("\s+", "", linea)

def paramFuncion(linea):
	param = re.split("PARAM", linea)
	if len(param)>1:
		if PROC:
			return "params["+param[1]+"]"
		else:
			sintaxError("Uso de la palabra reservada PARAM fuera de una funcion")
	return None

def asignacionAsignosa(variable, valor):
	creacionVariableValido(variable)
	param = paramFuncion(variable)
	if param:
		variable = param
	nombreVariableValido(variable)
	valor = nombreValorValido(valor)
	param = paramFuncion(valor)
	if param:
		valor = param
	variable = eliminarEspacios(variable)
	return variable, valor

def generarAsignacion(linea):
	if lineaVacia(linea): return ""
	asignacionIzq = re.split('<=', linea)
	asignacionDer = re.split('=>', linea)
	if len(asignacionIzq)>1:
		variable = re.split("VAR\(\s*(.*)\)", asignacionIzq[0])
		if len(variable) == 1: sintaxError("Asignacion de una variable sin el uso de VAR")
		variable = variable[1]
		valor = asignacionIzq[1]
	if len(asignacionDer)>1:
		variable = re.split("VAR\(\s*(.*)\)", asignacionDer[1])
		if len(variable) == 1: sintaxError("Asignacion de una variable sin el uso de VAR")
		variable = variable[1]
		valor =  asignacionDer[0]
	return asignacionAsignosa(variable, valor)

def revisarProcInicio(linea, PROC):
	nombre = re.sub("\)", "", linea)
	nombre = re.split("\$\^PROC\s*\(", nombre)
	if PROC and re.search("\$\^PROC", linea): sintaxError("Funcion dentro de funcion")
	if PROC: return PROC, None
	if re.search("\$\^PROC\s*\(", linea): return True, nombre[1]
	return False, None

def revisarProcFin(linea, PROC):
	if not PROC and re.search("\^\$", linea): sintaxError()
	if re.search("\^\$", linea): return False
	if PROC: return PROC
	return False

def revisarReturn(linea): 
	a = re.search("^(\s*)#", linea)
	if a:
		if not PROC:
			sintaxError("Return fuera de una funcion")
		b = a.span()
		c = nombreValorValido(linea[b[1]:])
		if c:
			return "return "+eliminarEspacios(c)
	return ""

def revisarIFELSE(linea):
	if re.search("^\s*IFELSE\s+", linea):
		newLinea = re.sub("\s*IFELSE\s+", "", linea)
		cortado = re.split("\)\s+|\s+\(", newLinea)
		return len(borrarNulos(cortado)) == 3
	return False

def agregarParentesis(linea, verificar = False):
	if verificar and not re.search("\(|\)", linea):
		return linea
	if not re.search("\(", linea):
		linea = "("+linea
	if not re.search("\)", linea):
		linea = linea+")"
	return linea

def formatearIFELESE(linea):
	newLinea = re.sub("\s*IFELSE\s+", "", linea)
	newLinea = re.split("\)\s+|\s+\(", newLinea)
	si = agregarParentesis(newLinea[0])
	condicion = agregarParentesis(newLinea[1], True)
	sino = agregarParentesis(newLinea[2])
	if llamadoProcValido(si) and llamadoProcValido(sino):
		si, sino = formatearLlamadoProc(si), formatearLlamadoProc(sino)
	if llamadoProcValido(condicion):
		condicion = formatearLlamadoProc(condicion)
	else:
		condicion = nombreValorValido(condicion)
	return si+" if "+condicion+" else "+sino

def escribirArchivo(nombreArchivo, datosNuevos):
	escribirData = open(nombreArchivo+".py", "w")
	for i in datosNuevos:
		print i,
		escribirData.write(i)
	return

def pseudoSwitch(linea, variablesLocales, variablesGlobales):
	retornoFuncion = revisarReturn(linea)
	if retornoFuncion: return retornoFuncion
	elif revisarCreacionVariable(linea):
		asignacion = generarAsignacion(linea)
		variablesLocales.append(asignacion[0])
		return " = ".join(asignacion)
	elif revisarReasignacionVariable(linea):
		asignacion = generarAsignacion(linea)
		if asignacion[0] not in variablesLocales and asignacion[0] not in variablesGlobales:
			sintaxError("La variable "+asignacion[0]+" no fue creada")
		return " = ".join(asignacion)
	elif llamadoProcValido(linea): return formatearLlamadoProc(linea)
	elif revisarIFELSE(linea): return formatearIFELESE(linea)
	return ""

nombreArchivo = getCommandName()
try:
	archivo = open(nombreArchivo)
except:
	IOerror("No se encontro el archivo llamado "+nombreArchivo+".")

datosNuevos = list()
datosNuevos.append("from stdlib import *\n\n")
variablesGlobales = list()
variablesLocales = list()

for i in archivo:
	NUMBERLINE += 1
	LINEAPROCESADA = i
	i = i.strip()
	PROC, nombreProc = revisarProcInicio(i, PROC)
	PROC = revisarProcFin(i, PROC)
	if re.search("^\s*\^\$\s*$", i): continue
	if PROC:
		if nombreProc:
			datosNuevos.append("def "+nombreProc+"(*params):")
		else:
			datosNuevos.append("\t")
			datosNuevos.append(pseudoSwitch(i, variablesLocales, variablesGlobales))
	else:
		variablesLocales = list()
		datosNuevos.append(pseudoSwitch(i, variablesGlobales, variablesGlobales))
	datosNuevos.append("\n")
archivo.close()

escribirArchivo(nombreArchivo, datosNuevos)
print "Se ha creado el archivo "+nombreArchivo+".py"+" de forma satisfactoria"
