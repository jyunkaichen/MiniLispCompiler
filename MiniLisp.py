import sys,copy

vardic = {}
global callfunc
callfunc = False

class Function(object):
	def __init__(self, ids, body, fc):
		self.ids = ids
		self.body = body
		self.fc = fc

def split_input(Input): 
	tokens = Input.replace('(',' ( ').replace(')',' ) ').split()
	return tokens

def typing_tokens(tokens): 
	temp = tokens.pop(0)
	if temp == '(':
		FT = [] #final tokens
		while tokens[0] != ')':
			FT.append(typing_tokens(tokens))
		tokens.pop(0)
		return FT
	else:
		return get_type(temp)

def get_type(token):
	if(token.isdigit()):
		return int(token)
	else: return str(token)

def exe(FT,d):
	# number & bool-val
	if isinstance(FT,int): return FT
	elif isinstance(FT,str):
			global callfunc
			if FT == "#t": 
				return True
			elif FT == "#f": 
				return False
			elif callfunc:
				return d[FT]
			elif FT in vardic:
				if type(FT) == type(Function([],[],False)):
					if (len(vardic[FT].ids)) == 0:
						return vardic[FT].body
				return vardic[FT]
			elif FT == '+' or FT == '-' or FT == '*' or FT == '/' or FT == 'mod' or FT == '>' or FT == '<' or FT == '=' or FT == 'and' or FT == 'or' or FT == 'not' or FT == 'if' or FT == 'define' or FT == 'fun':
				print('syntax error')
				return "False"
			elif int(FT): 
				return int(FT)
			else: 
				print('syntax error')
				return "False"
	elif len(FT) == 1:
		tmp = exe(FT[0],d)
		if isinstance(tmp,int):
			return tmp
	# DEFINE
	elif FT[0] == "define":
		if not len(FT) == 3:
			print('syntax error')
			return "False"
		else:
			vardic[FT[1]] = exe(FT[2],d)
	# PRINT
	elif FT[0] == "print-num":
		if len(FT) > 2:
			print('syntax error')
			return "False"
		else:
			tmp = exe(FT[1],d)
			if isinstance(tmp,bool):	
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			elif isinstance(tmp,int):
				print(tmp)
			elif type(tmp) == type(Function([],[],False)):
				print("Type Error: Expect 'number' but got 'function'")
				return "False"
			elif tmp == 'False':
				return "False"
	elif FT[0] == "print-bool":
		if len(FT) > 2:
			print('syntax error')
			return "False"
		else:
			tmp = exe(FT[1],d)
			if isinstance(tmp,bool):
				if tmp: print("#t")
				else: print("#f") 
			elif isinstance(tmp,int): 
				print("Type Error: Expect 'boolean' but got 'number'")
				return "False"	
			elif type(tmp) == type(Function([],[],False)):
				print("Type Error: Expect 'boolean' but got 'function'")
				return "False"
			elif tmp == "False":
				return "False"
	# numerical oprations
	elif FT[0] == '+':
		if len(FT) < 3: 
			print('syntax error')
			return "False"
		FT.pop(0)
		ans = 0
		for i in range(0,len(FT)):
			tmp = exe(FT[i],d)
			if isinstance(tmp,bool):
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			elif isinstance(tmp,int):
				ans += tmp
		return ans
	elif FT[0] == '-':
		if not len(FT) == 3: 
			print('syntax error')
			return "False"
		else: 
			tmp1 = exe(FT[1],d)
			tmp2 = exe(FT[2],d)
			if isinstance(tmp1,bool) or isinstance(tmp2,bool):
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			elif isinstance(tmp1,int) and isinstance(tmp2,int):
				return tmp1-tmp2
	elif FT[0] == '*':
		if len(FT) < 3: 
			print('syntax error')
			return "False"
		FT.pop(0)
		ans = 1
		for i in range(0,len(FT)):
			tmp = exe(FT[i],d)
			if isinstance(tmp,bool):
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			elif isinstance(tmp,int):
				ans *= tmp
		return ans
	elif FT[0] == '/':
		if not len(FT) == 3: 
			print('syntax error')
			return "False"
		else: 
			tmp1 = exe(FT[1],d)
			tmp2 = exe(FT[2],d)
			if isinstance(tmp1,bool) or isinstance(tmp2,bool):
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			if isinstance(tmp1,int) and isinstance(tmp2,int):
				return int(tmp1/tmp2)
	elif FT[0] == 'mod':
		if not len(FT) == 3: 
			print('syntax error')
			return "False"
		else: 
			tmp1 = exe(FT[1],d)
			tmp2 = exe(FT[2],d)
			if isinstance(tmp1,bool) or isinstance(tmp2,bool):
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			if isinstance(tmp1,int) and isinstance(tmp2,int):
				return int(tmp1%tmp2)
	elif FT[0] == '>':
		if not len(FT) == 3: 
			print('syntax error')
			return "False"
		else: 
			tmp1 = exe(FT[1],d)
			tmp2 = exe(FT[2],d)
			if isinstance(tmp1,bool) or isinstance(tmp2,bool):
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			elif isinstance(tmp1,int) and isinstance(tmp2,int):
				return tmp1>tmp2
	elif FT[0] == '<':
		if not len(FT) == 3: 
			print('syntax error')
			return "False"
		else: 
			tmp1 = exe(FT[1],d)
			tmp2 = exe(FT[2],d)
			if isinstance(tmp1,bool) or isinstance(tmp2,bool):
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			elif isinstance(tmp1,int) and isinstance(tmp2,int):
				return tmp1<tmp2
	elif FT[0] == '=':
		if len(FT) < 3: 
			print('syntax error')
			return "False"
		FT.pop(0)
		tmp1 = exe(FT[0],d)
		if isinstance(tmp1,bool):
			print("Type Error: Expect 'number' but got 'boolean'")
			return "False"
		FT.pop(0)
		for i in range(len(FT)):
			tmp2 = exe(FT[i],d)
			if isinstance(tmp2,bool):
				print("Type Error: Expect 'number' but got 'boolean'")
				return "False"
			elif isinstance(tmp2,int):
				if tmp1 != tmp2: return False 
		return True
	# logical oprations
	elif FT[0] == 'and':
		if len(FT) < 3: 
			print('syntax error')
			return "False"
		FT.pop(0)
		tmp1 = exe(FT[0],d)
		if not isinstance(tmp1,bool):
			print("Type Error: Expect 'boolean' but got 'number'")
			return "False"
		FT.pop(0)
		for i in range(len(FT)):
			tmp2 = exe(FT[i],d)
			if isinstance(tmp2,bool):
				tmp1 = tmp1 and tmp2  
			else: 
				print("Type Error: Expect 'boolean' but got 'number'")
				return "False"
		return 	tmp1
	elif FT[0] == 'or':
		if len(FT) < 3: 
			print('syntax error')
			return "False"
		FT.pop(0)
		tmp1 = exe(FT[0],d)
		if not isinstance(tmp1,bool):
			print("Type Error: Expect 'boolean' but got 'number'")
			return "False"
		FT.pop(0)
		for i in range(len(FT)):
			tmp2 = exe(FT[i],d)
			if isinstance(tmp2,bool):
				tmp1 = tmp1 or tmp2  
			else: 
				print("Type Error: Expect 'boolean' but got 'number'")
				return "False"
		return 	tmp1
	elif FT[0] == 'not':
		if not len(FT) == 2: 
			print('syntax error')
			return "False"
		else: 
			tmp = exe(FT[1],d)
			if isinstance(tmp,bool):
				return not tmp 
			else: 
				print("Type Error: Expect 'boolean' but got 'number'")
				return "False"
	# if 
	elif FT[0] == 'if':
		if not len(FT) == 4: 
			print('syntax error')
			return "False"
		else: 
			tmp = exe(FT[1],d) 
			if not isinstance(tmp,bool):
				print("Type Error: Expect 'boolean' but got 'number'")
				return "False" 
			else: 
				if tmp: return exe(FT[2],d)
				else: return exe(FT[3],d)
	# fucexp
	elif FT[0] == "fun":
		func = Function([],[],False)
		if len(FT) > 3: #nest function
			a = []
			for i in range(2,len(FT)-1):
				if FT[i][0] == 'define':
					a.append(FT[i])
				else:
					print('syntax error')
					return "False"
			a.append(FT[len(FT)-1])
			func.ids = FT[1]
			func.body = a
			return func
		elif len(FT) == 3:
			if len(FT[1]) == 0: # case: (fun () 2)
				if isinstance(exe(FT[2],d),int):
					func.body = exe(FT[2],d)
				return func.body
			for i in range(len(FT[1])):
				func.__dict__[FT[1][i]] = 0
			if FT[2][0] == "fun":
				func.fc = True
			func.ids = FT[1]
			func.body = FT[2]
			return func
		else: 
			print('syntax error')
			return "False"
	# fuccall
	elif FT[0][0] == "fun":
		callfunc = True
		if len(FT) < 2:
			print('syntax error')
			return "False"
		else:
			F = copy.deepcopy(exe(FT[0],d))
			tmpid = FT[0][1]
			if len(tmpid) == 0:
				return int(F.body)
			FT.pop(0)
			tmp = len(FT)
			for i in range(0,tmp):
				F.__dict__[tmpid[i]] = exe(FT[0],d)
				FT.pop(0)
			ans = exe(F.body,F.__dict__)
			callfunc = False
			return ans
	elif isinstance(FT[0],str):
		if FT[0] in vardic:
			if type(vardic[FT[0]]) == type(Function([],[],False)):
				callfunc = True
				if not len(FT)-1 == len(vardic[FT[0]].ids):
					print('syntax error')
					return "False"
				else:
					F = copy.deepcopy(vardic[FT[0]]) 
					tmpid = F.ids
					if len(tmpid) == 0:
						return int(F.body)
					FT.pop(0)

					### store ids' value
					if len(FT) == 1: 
						if type(FT[0]) == type(Function([],[],False)):
							if len(FT[0]) == 1:
								F.__dict__[tmpid[0]] = exe(FT[0][0],d)
								tmp = 0
						else:
							tmp = len(FT)
					else:
						tmp = len(FT)

					for i in range(0,tmp):
						F.__dict__[tmpid[i]] = exe(FT[0],d)
						if type(F.__dict__[tmpid[i]]) == type(Function([],[],False)): # first-class function
							vardic[tmpid[i]] = F.__dict__[tmpid[i]]
						FT.pop(0)

					### calculate function's value
					if not isinstance(F.body[0],list): # normal function
						if F.fc == True: # first-class function
							func = Function([],[],False)
							func.ids = F.body[1]
							for i in range(0,len(F.body[2])):
								if F.body[2][i] in F.__dict__:
									F.body[2][i] = F.__dict__[F.body[2][i]]
							func.body = F.body[2]
							return func
						ans = exe(F.body,F.__dict__)
					else: # nest function
						for i in range(0,len(F.body)-1):
							exe(F.body[i],d)
							l = len(F.body)
						ans = exe(F.body[l-1],F.__dict__)
					callfunc = False
					return ans
			else:
				print('syntax error')
				return "False"
		else:
			print('syntax error')
			return "False"

	# else grammar
	else:
		print('syntax error')
		return "False"

# file input
f = open('test.txt','r')
finalline = ''
l = f.readlines()

for line in range(0,len(l)):
	if not len(l[line]) == 1:
		if l[line][0] == ' ' or l[line][0] == '\t':
			l[line] = l[line].replace('\n',' ')
			finalline += l[line]
		else:
			l[line] = l[line].replace('\n',' ')
			finalline += l[line]
			if l[line+1] == '\n':
				exe(typing_tokens(split_input(finalline)),vardic)
				finalline = ''
			elif not len(l[line+1]) == 0:
				if l[line+1][0] == ' ' or l[line+1][0] == '\t':
					continue
				else: 
					exe(typing_tokens(split_input(finalline)),vardic)
					finalline = ''
	elif len(l[line]) == 1: #space line
		if not len(finalline) == 0:
			exe(typing_tokens(split_input(finalline)),vardic)
			finalline = ''

# manually input
while True:
	a = exe(typing_tokens(split_input(input())),vardic)
	if a == 'False':
		continue