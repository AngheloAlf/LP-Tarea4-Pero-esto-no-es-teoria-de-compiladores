import sys, re
#print sys.argv[1:]

def getCommandName():
	if sys.argv[1:]:
		nombre = " ".join(sys.argv[1:])
		return nombre
	else:
		return "alf.alf"

def revisarAsignacion(i):
	weaOriginal = i.strip()
	asignacion = re.search('<=', weaOriginal)
	if asignacion == None:
		return
	a = weaOriginal[:asignacion.span()[0]]
	b = weaOriginal[asignacion.span()[1]:]
	buscando = re.search("VAR", a)
	c = a[buscando.span()[1]:]
	variable = re.split("\(\s*(.*)\s*\)", c)[1]
	d = re.sub("\s*","",b)
	return variable+" = "+d

nombre = getCommandName()
datosNuevos = list()
datosNuevos.append("from stdlib import *\n")

try:
	archivo = open(nombre)
	for i in archivo:
		print revisarAsignacion(i)
except:
	raise
# except IOError, (errno, strerror) :
# 	print "I/O error(%s) : %s " % ( errno , strerror)
# except ValueError :
# 	print " Could not convert data to an integer. "
# except:
# 	print "Unexpected error: " , sys.exc_info()[0]
# 	raise