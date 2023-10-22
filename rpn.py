from utils import *

def precedence(s):
	if s == '(':
		return 0
	elif s == '!':
		return 4
	elif s == '+':
		return 3
	elif s == '|':
		return 2
	elif s == '^':
		return 1
	else:
		return 99

def is_operator(s):
	if s == '+' or s == '|' or s == '^' or s == '!':
		return 1
	else:
		return (-1)

def convertPolish(infix):
	re = []
	temp = []
	for i in infix :
		if i == '(':
			temp.append(i)
		elif i == ')':
			if len(temp) > 0:
				next = temp.pop()
			while next != '(':
				re.append(next)
				next = temp.pop()
		elif is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", i) > -1:
			re.append(i)
		elif is_operator(i) == 1:
			p = precedence(i)
			while len(temp) != 0 and p <= precedence(temp[-1]):
				re.append(temp.pop())
			temp.append(i)
		else:
			continue
	while len(temp) > 0 :
		re.append(temp.pop())
	return ''.join(re)

def RPN(g):
	arg = 0
	r = []

	for st in range(len(g)):
		try:
			r[st]
		except:
			r.append([])
		for i in range(len(g[st])):
			if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ!", g[st][i]) > -1:
				arg += 1
			if g[st][i] == '=':
				if g[st][i - 1] == '<':
					tmp = i - 1
				else:
					tmp = i
				if arg == 1:
					while (tmp > 0 and is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][tmp]) == -1):
						tmp -= 1
					r[st].append(g[st][tmp])
				else:
					r[st].append(convertPolish(g[st][:tmp]))
			if (g[st][i - 1] == '>'):
				tmp = i
				arg = 0
				while (tmp < len(g[st])):
					if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ!", g[st][i]) > -1:
						arg += 1
					tmp += 1
				tmp = i
				if arg == 1:
					while (tmp < len(g[st]) and is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][tmp]) == -1):
						tmp += 1
					r[st].append(g[st][tmp])
				else:
					r[st].append(convertPolish(g[st][i:]))
	for st in range(len(g)):
		i = len(g)
		if (g[st].find("<") > -1):
			try:
				r[i]
			except:
				r.append([])
			r[i].append(r[st][1])
			r[i].append(r[st][0])
			i += 1
	return (r)
