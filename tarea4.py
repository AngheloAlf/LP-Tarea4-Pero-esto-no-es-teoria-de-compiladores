import re
from generalFunctions import *
from traductorFunctions import *

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
	errorAux.NUMBERLINE += 1
	errorAux.LINEAPROCESADA = i
	i = i.strip()
	proc.PROC, nombreProc = revisarProcInicio(i, proc.PROC)
	proc.PROC = revisarProcFin(i, proc.PROC)
	if re.search("^\s*\^\$\s*$", i): continue
	if proc.PROC:
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
