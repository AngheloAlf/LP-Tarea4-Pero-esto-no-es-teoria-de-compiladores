from generalFunctions import *
from traductorFunctions import *


def pseudo_switch(linea, variableslocales, variablesglobales):
    retorno_funcion = revisarReturn(linea)
    if retorno_funcion:
        return retorno_funcion
    elif revisarCreacionVariable(linea):
        asignacion = generarAsignacion(linea)
        variablesLocales.append(asignacion[0])
        return " = ".join(asignacion)
    elif revisarReasignacionVariable(linea):
        asignacion = generarAsignacion(linea)
        if asignacion[0] not in variableslocales and asignacion[0] not in variablesglobales:
            sintax_error("La variable "+asignacion[0]+" no fue creada")
        return " = ".join(asignacion)
    elif llamadoProcValido(linea):
        return formatearLlamadoProc(linea)
    elif revisarIFELSE(linea):
        return formatearIFELESE(linea)
    return ""

nombreArchivo = get_command_name()
archivo = ""
try:
    archivo = open(nombreArchivo)
except IOError:
    ioerror("No se encontro el archivo llamado "+nombreArchivo+".")

datosNuevos = list()
datosNuevos.append("from stdlib import *\n\n")
variablesGlobales = list()
variablesLocales = list()

for i in archivo:
    ErrorAux.NUMBERLINE += 1
    ErrorAux.LINEAPROCESADA = i
    i = i.strip()
    proc.PROC, nombreProc = revisarProcInicio(i, proc.PROC)
    proc.PROC = revisarProcFin(i, proc.PROC)
    if re.search("^\s*\^\$\s*$", i):
        continue
    if proc.PROC:
        if nombreProc:
            datosNuevos.append("def "+nombreProc+"(*params):")
        else:
            datosNuevos.append("\t")
            datosNuevos.append(pseudo_switch(i, variablesLocales, variablesGlobales))
    else:
        variablesLocales = list()
        datosNuevos.append(pseudo_switch(i, variablesGlobales, variablesGlobales))
    datosNuevos.append("\n")
archivo.close()

escribir_archivo(nombreArchivo, datosNuevos)
print "Se ha creado el archivo "+nombreArchivo+".py"+" de forma satisfactoria"
