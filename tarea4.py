import sys, re
#print sys.argv[1:]

def getCommandName():
	if sys.argv[1:]:
		nombre = " ".join(sys.argv[1:])
		return nombre
	else:
		return "alf.alf"

def revisarAsignacion(leseraOriginal):
	return re.search('<=', leseraOriginal) or re.search('=>', leseraOriginal)

def generarAsignacion(leseraOriginal):
	def asignacionAsignosa(variable, valor):
		buscando = re.search("VAR", variable)
		c = variable[buscando.span()[1]:]
		variable = re.split("\(\s*(.*)\)", c)
		variable = variable[1]
		valor = re.sub("\s*","",valor)
		return variable+" = "+valor
	asignacionIzq = re.search('<=', leseraOriginal)
	asignacionDer = re.search('=>', leseraOriginal)
	if asignacionIzq:
		variable = leseraOriginal[:asignacionIzq.span()[0]]
		valor = leseraOriginal[asignacionIzq.span()[1]:]
		return asignacionAsignosa(variable, valor)

	if asignacionDer:
		variable = leseraOriginal[asignacionDer.span()[1]:]
		valor = leseraOriginal[:asignacionDer.span()[0]]
		return asignacionAsignosa(variable, valor)

	return None



nombre = getCommandName()
datosNuevos = list()
datosNuevos.append("from stdlib import *\n")


archivo = open(nombre)
for i in archivo:
	if revisarAsignacion(i.strip()):
		datosNuevos.append(generarAsignacion(i.strip())+"\n")

print datosNuevos
# except IOError, (errno, strerror) :
# 	print "I/O error(%s) : %s " % ( errno , strerror)
# except ValueError :
# 	print " Could not convert data to an integer. "
# except:
# 	print "Unexpected error: " , sys.exc_info()[0]
# 	raise