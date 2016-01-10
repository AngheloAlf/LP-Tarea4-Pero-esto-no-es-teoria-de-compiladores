def EQ(A, B):
	return A == B

def NEQ(A, B):
	return not EQ(A, B)

def LT(A, B):
	if A < B: return True
	else: return False

def GT(A, B):
	return not LEQ(A, B)

def LEQ(A, B):
	if A <= B: return True
	else: return False

def GEQ(A, B):
	return not LT(A, B)

def ADD(A, B):
	return A + B

def SUB(A, B):
	return A - B

def INPUT():
	return int(raw_input(""))

def OUTPUT(OUT):
	print OUT
