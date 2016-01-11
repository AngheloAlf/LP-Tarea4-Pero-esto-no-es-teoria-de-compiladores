import re
from generalFunctions import sintax_error, borrar_nulos


class Proc:
    def __init__(self):
        pass
    PROC = False


def llamado_proc_valido(linea):
    cortado = re.split("\((.*)\)", linea)
    if cortado and len(cortado) > 1:
        if re.search("\(|\)", cortado[1]):
            sintax_error("Se realizo llamado de funcion dentro de llamado de funcion")
        return True
    return False


def formatear_llamado_proc(linea):
    if re.search("\(\s*\)", linea):
        return "pass"
    a = re.split("\((.*)\)", linea)[1]
    b = re.split("\s", a)
    return b[0]+"("+", ".join(map(nombre_valor_valido, b[1:]))+")"


def creacion_variable_valido(linea):
    if re.search("^PARAM[0-9]+$", linea):
        sintax_error("Uso de nombre reservado para creacion de variable")
    return


def nombre_variable_valido(linea):
    if len(borrar_nulos(re.split("\s*", linea))) != 1:
        if len(re.split("[^a-zA-Z]*", linea)) != 1:
            sintax_error("Uso de caracteres no permitidos para una variable")
    return


def nombre_valor_valido(linea):
    if linea_vacia(linea):
        sintax_error("No hay valor para asignar a la variable")
    elif re.search("^PARAM[0-9]+$", linea):
        return "params["+re.split("PARAM", linea)[1]+"]"
    elif revisarifelse(linea):
        return formatearifelse(linea)
    elif llamado_proc_valido(linea):
        return formatear_llamado_proc(linea)
    elif len(re.split("^TRUE$", linea)) == 2:
        return "True"
    elif len(re.split("^FALSE$", linea)) == 2:
        return "False"
    elif len(re.split("[[\-0-9]*|[0-9]*]", linea)) == 2:
        return eliminar_espacios(linea)
    elif not nombre_variable_valido(linea):
        return eliminar_espacios(linea)
    else:
        sintax_error("Asignacion de variable invalida")
    return


def revisar_creacion_variable(linea):
    return re.search('^VAR\((.*)\)(.*)\s+<=\s+(.*)$', linea) or re.search('^(.*)\s+=>\s+VAR\((.*)\)$', linea)


def linea_vacia(linea):
    return re.search("^\s*$", linea)


def revisar_reasignacion_variable(linea):
    if re.search("VAR", linea):
        return False
    return re.search('^(.*)<=(.*)$', linea) or re.search('^(.*)=>(.*)$', linea)


def eliminar_espacios(linea):
    return re.sub("\s+", "", linea)


def param_funcion(linea):
    param = re.split("PARAM", linea)
    if len(param) > 1:
        if Proc.PROC:
            return "params["+param[1]+"]"
        else:
            sintax_error("Uso de la palabra reservada PARAM fuera de una funcion")
    return 


def asignacion_asignosa(variable, valor):
    creacion_variable_valido(variable)
    param = param_funcion(variable)
    if param:
        variable = param
    nombre_variable_valido(variable)
    valor = nombre_valor_valido(valor)
    param = param_funcion(valor)
    if param:
        valor = param
    variable = eliminar_espacios(variable)
    return variable, valor


def generar_asignacion(linea):
    if linea_vacia(linea):
        return ""
    asignacion_izq = re.split('<=', linea)
    asignacion_der = re.split('=>', linea)
    valor, variable = "", ""
    if len(asignacion_izq) > 1:
        variable = re.split("VAR\(\s*(.*)\)", asignacion_izq[0])
        if len(variable) == 1:
            sintax_error("Asignacion de una variable sin el uso de VAR")
        variable = variable[1]
        valor = asignacion_izq[1]
    elif len(asignacion_der) > 1:
        variable = re.split("VAR\(\s*(.*)\)", asignacion_der[1])
        if len(variable) == 1:
            sintax_error("Asignacion de una variable sin el uso de VAR")
        variable = variable[1]
        valor = asignacion_der[0]
    return asignacion_asignosa(variable, valor)


def revisar_proc_inicio(linea, proc):
    nombre = re.sub("\)", "", linea)
    nombre = re.split("\$\^PROC\s*\(", nombre)
    if proc and re.search("\$\^PROC", linea):
        sintax_error("Funcion dentro de funcion")
    if proc:
        return proc, None
    if re.search("\$\^PROC\s*\(", linea):
        return True, nombre[1]
    return False, None


def revisar_proc_fin(linea, proc):
    if not proc and re.search("\^\$", linea):
        sintax_error("Cierre de funcion sin entrar en ella")
    if re.search("\^\$", linea):
        return False
    if proc:
        return proc
    return False


def revisar_return(linea):
    a = re.search("^(\s*)#", linea)
    if a:
        if not Proc.PROC:
            sintax_error("Return fuera de una funcion")
        b = a.span()
        c = nombre_valor_valido(linea[b[1]:])
        if c:
            return "return "+eliminar_espacios(c)
    return ""


def revisarifelse(linea):
    if re.search("^\s*IFELSE\s+", linea):
        newlinea = re.sub("\s*IFELSE\s+", "", linea)
        cortado = re.split("\)\s+|\s+\(", newlinea)
        return len(borrar_nulos(cortado)) == 3
    return False


def agregar_parentesis(linea, verificar=False):
    if verificar and not re.search("\(|\)", linea):
        return linea
    if not re.search("\(", linea):
        linea = "("+linea
    if not re.search("\)", linea):
        linea += ")"
    return linea


def formatearifelse(linea):
    newlinea = re.sub("\s*IFELSE\s+", "", linea)
    newlinea = re.split("\)\s+|\s+\(", newlinea)
    si = agregar_parentesis(newlinea[0])
    condicion = agregar_parentesis(newlinea[1], True)
    sino = agregar_parentesis(newlinea[2])
    if llamado_proc_valido(si) and llamado_proc_valido(sino):
        si, sino = formatear_llamado_proc(si), formatear_llamado_proc(sino)
    if llamado_proc_valido(condicion):
        condicion = formatear_llamado_proc(condicion)
    else:
        condicion = nombre_valor_valido(condicion)
    return si+" if "+condicion+" else "+sino
