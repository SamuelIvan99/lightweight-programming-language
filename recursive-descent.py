import string

# Write your program here
program = """
char  m y _ v a r  =  1 0  ;
"""

tokens = program.strip("\n").split(" ")
print(tokens)

def match(expected_tokens):
	look_ahead = tokens[0]
	if look_ahead in expected_tokens:
		tokens.pop(0)
	else:
		print(f"Syntax error: expected {expected_tokens} got {look_ahead}")
		exit()

def Start():
	Declare()
	match([";"])
	print("Parsing completed!")

def Declare():
	Type()
	match([""])
	Var()
	match([""])
	match(["="])
	match([""])
	ValPlus()
	match([""])

def Var():
	look_ahead = tokens[0]
	if look_ahead in list(string.ascii_lowercase) or \
		look_ahead in list(string.ascii_uppercase) or \
		look_ahead in ["_"]:
		VarFirst()
		VarRestStar()

def VarRestStar():
	look_ahead = tokens[0]
	if look_ahead in list(string.ascii_lowercase) or \
		look_ahead in list(string.ascii_uppercase) or \
		look_ahead in list(string.digits) or \
		look_ahead in ["_", "-"]:
		VarRest()
		VarRestStar()

def VarRest():
	look_ahead = tokens[0]
	if look_ahead in list(string.ascii_lowercase) or \
		look_ahead in list(string.ascii_uppercase) or \
		look_ahead in list(string.digits):
		AlphaNum()
	elif look_ahead in ["_", "-"]:
		match(["_", "-"])

def VarFirst():
	look_ahead = tokens[0]
	if look_ahead in list(string.ascii_lowercase) or \
		look_ahead in list(string.ascii_uppercase):
		Alpha()
	elif look_ahead in ["_"]:
		match(["_"])

def ValPlus():
	look_ahead = tokens[0]
	if look_ahead in list(string.digits):
		Digit()
		ValPlus()

def AlphaNum():
	look_ahead = tokens[0]
	if look_ahead in list(string.ascii_lowercase) or \
		look_ahead in list(string.ascii_uppercase):
		Alpha()
	elif look_ahead in list(string.digits):
		Digit()
	else:
		print("Syntax error: expected a letter in range a..Z or a digit in range 0..9")
		exit()

def Alpha():
	look_ahead = tokens[0]
	if look_ahead in list(string.ascii_lowercase):
		Lower()
	elif look_ahead in list(string.ascii_uppercase):
		Upper()
	else:
		print("Syntax error: expected a letter in range a..Z")		
		exit()

def Digit():
	match(list(string.digits))

def Lower():
	match(list(string.ascii_lowercase))

def Upper():
	match(list(string.ascii_uppercase))

def Type():
	look_ahead = tokens[0]
	if look_ahead in ["i64", "i32"]:
		IType()
	elif look_ahead in ["u64", "u32"]:
		UType()
	elif look_ahead in ["char"]:
		match(["char"])
	else:
		print("Syntax error: expected char, i64, i32, u64, u32")
		exit()

def IType():	
	match(["i64", "i32"])

def UType():
	match(["u64", "u32"])

def main():
	Start()

if __name__ == '__main__':
	main()
