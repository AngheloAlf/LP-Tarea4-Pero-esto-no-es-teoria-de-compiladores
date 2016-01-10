from stdlib import *

def Dummy(*params):
	return 1024

def CaseA(*params):
	return 42

def CaseB(*params):
	return Dummy()

def Default(*params):
	return 0

def IfCaseB(*params):
	Res = CaseB() if EQ(params[0], 2) else Default()
	return Res

def Switch(*params):
	Res = CaseA() if EQ(params[0], 1) else IfCaseB(params[0])
	return Res

def same(*params):
	return params[0]

def multi(*params):
	a = params[0]
	c = SUB(params[1], 1)
	d = same(a) if EQ(c, 1) else multi(a, c)
	return ADD(d,a)

In = INPUT()
Res = Switch(In)
Res = ADD(Res, 5)
OUTPUT(Res)

ejemplo = multi(8, 9)
OUTPUT(ejemplo)
