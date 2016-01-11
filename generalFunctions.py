import sys


class ErrorAux:
    def __init__(self):
        pass
    NUMBERLINE = 0
    LINEAPROCESADA = ""


def ioerror(mensaje="Error desconocido"):
    print " -- I/O ERROR -- \n"+mensaje
    exit(0)
    return


def sintax_error(mensaje="Error desconocido"):
    print " -- ERROR de sintaxis. -- \nLinea:", ErrorAux.NUMBERLINE, "\n"+ErrorAux.LINEAPROCESADA+"\n"+mensaje
    exit(0)
    return


def get_command_name():
    if sys.argv[1:]:
        return " ".join(sys.argv[1:])
    else:
        ioerror("No se ingreso un archivo para traducir.")


def borrar_nulos(lista):
    return [x for x in lista if x]


def escribir_archivo(nombre_archivo, datos_nuevos):
    escribir_data = open(nombre_archivo+".py", "w")
    for i in datos_nuevos:
        escribir_data.write(i)
    return
