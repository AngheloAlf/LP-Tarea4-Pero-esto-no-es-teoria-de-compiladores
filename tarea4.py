from generalFunctions import *
from traductorFunctions import *


def pseudo_switch(linea, variableslocales, variablesglobales):
    retorno_funcion = revisar_return(linea)
    if retorno_funcion:
        return retorno_funcion
    elif revisar_creacion_variable(linea):
        asignacion = generar_asignacion(linea)
        variablesLocales.append(asignacion[0])
        return " = ".join(asignacion)
    elif revisar_reasignacion_variable(linea):
        asignacion = generar_asignacion(linea)
        if asignacion[0] not in variableslocales and asignacion[0] not in variablesglobales:
            sintax_error("La variable "+asignacion[0]+" no fue creada")
        return " = ".join(asignacion)
    elif llamado_proc_valido(linea):
        return formatear_llamado_proc(linea)
    elif revisarifelse(linea):
        return formatearifelse(linea)
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
    Proc.PROC, nombreProc = revisar_proc_inicio(i, Proc.PROC)
    Proc.PROC = revisar_proc_fin(i, Proc.PROC)
    if re.search("^\s*\^\$\s*$", i):
        continue
    if Proc.PROC:
        if nombreProc:
            datosNuevos.append("\ndef "+nombreProc+"(*params):")
        else:
            datosNuevos.append("    ")
            datosNuevos.append(pseudo_switch(i, variablesLocales, variablesGlobales))
    else:
        variablesLocales = list()
        datosNuevos.append(pseudo_switch(i, variablesGlobales, variablesGlobales))
    datosNuevos.append("\n")
archivo.close()

escribir_archivo(nombreArchivo, datosNuevos)
print "Se ha creado el archivo "+nombreArchivo+".py"+" de forma satisfactoria"
