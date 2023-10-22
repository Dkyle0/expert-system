import sys
import os
from rpn import RPN
from proc import mf
from utils import *

def f_in_list(g, st):
	for i in range(len(g)):
		if (type(g[i]) == str and g[i].find(st) > -1):
			return (1)
	return (0)

def remover(g):
	while(f_in_list(g, "-del") == 1):
		g.remove("-del")

def read_add_error(filepath):
	if not os.path.isfile(filepath):
		error_exit("Invalid filepath")
	if not os.access(filepath, os.R_OK):
		error_exit("file has no read permissions")
	allowedSymbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ()+!|^<=>?# '
	try:
		with open(filepath, 'r') as f:
			read = f.readlines()
	except:
		error_exit("can't read file")
	g = []
	for i in range(len(read)):
		if read[i][0] != '\n':
			g.append(read[i].strip())
	for i in range(len(g)):
		if (len(g) > 100000):
			error_exit("many lines")
		for i2 in range(len(g[i])):
			if (len(g[i]) > 100000):
				error_exit("long line")
			if is_simbol_in_str(allowedSymbols , g[i][i2]) == -1:
				if (g[i].find('#') < i2 and g[i].find('#') != -1):
					pass
				else:
					error_exit("Invalid simbol: '" + g[i][i2] + "'")
	for i in range(len(g)):
		c = g[i].find('#')
		if c > -1:
			if c != 0:
				g[i] = g[i][0:c]
			else:
				g[i] = "-del"
	remover(g)
	return (g)

def parse_queries_and_facts(g, ar):
	c = 0
	allowedSymbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
	r = ""
	for i in range(len(g)):
		if (g[i][0]) == ar:
			c += 1
	if c != 1:
		if ar == '?':
			error_exit("Invalid queries")
		else:
			error_exit("Invalid fact")
	else:
		c = 0
		for i in range(len(g)):
			if (g[i][0]) == ar:
				for a in range(len(g[i])):
					if (g[i][a]) == ar:
						c += 1
				if c != 1:
					if ar == '?':
						error_exit("Invalid queries")
					else:
						error_exit("Invalid fact")
				else:
					r = g[i][1:len(g[i])]
					g[i] = "-del"
		for i in range(len(r)):
			if allowedSymbols.find(r[i]) == -1:
				if ar == '?':
					error_exit("Invalid queries")
				else:
					error_exit("Invalid fact")	
	return (r)

def deep_check(g):
	for st in range(len(g)):
		arg = 0
		for i in range(len(g[st])):
			if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][i]) > -1:
				if (i > 0):
					t = i - 1
					while(g[st][t] == ' '):
						t -= 1
					if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][t]) > -1:
						error_exit("Invalid rules 1")
				t = i
				if (i + 1 < len(g[st])):
					t = i + 1
				while(t < len(g[st]) and g[st][t] == ' '):
					t += 1
				if t + 1 < len(g[st]):
					if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][t]) > -1:
						error_exit("Invalid rules 2")
			if (g[st][i] == '!'):
				if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ(", g[st][i + 1]) == -1:
					error_exit("Invalid rules 3")
			if (g[st][i] == '+' or g[st][i] == '|' or g[st][i] == '^'):
				if (i) == 0:
					error_exit("Invalid rules 4")
				t = i - 1
				while(g[st][t] == ' '):
					t -= 1
				if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ)", g[st][t]) == -1:
					error_exit("Invalid rules 4")
				if (i + 1 < len(g[st])):
					t = i + 1
				else:
					error_exit("Invalid rules")
				while(g[st][t] == ' ' and len(g[st])):
					t += 1
				if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ(!", g[st][t]) == -1:
					error_exit("Invalid rules 5")
			if (g[st][i] == '<'):
				if g[st][i + 1] != '=':
					error_exit("Invalid rules 6")
			if (g[st][i] == '('):
				if (i + 1 < len(g[st])):
					t = i + 1
				else:
					error_exit("Invalid rules 7")
				while(t < len(g[st]) and  g[st][t] != ')'):
					if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][t]) > -1:
						arg += 1
					t += 1
				if (arg < 1):
					error_exit("Invalid rules 8")

def check_rule(g):
	for st in range(len(g)):
		rav = 0
		arg = 0
		br_o = 0
		br_c = 0
		pt2 = 0
		for i in range(len(g[st])):
			if (g[st][i] == '='):
				rav += 1
				if (g[st][i + 1] != '>'):
					error_exit("Invalid rules")
		if rav != 1:
			error_exit("Invalid rules")
		for i in range(len(g[st])):
			if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][i]) > -1:
				arg += 1
			if g[st][i] == '>':
				pt2 = i + 1
				break
			if g[st][i] == '(':
				br_o += 1
			if g[st][i] == ')':
				br_c += 1
		if br_o != br_c:
			error_exit("Invalid rules")
		if arg < 1:
			error_exit("Invalid rules")
		arg = 0
		while (pt2 < len(g[st])):
			if g[st][pt2] == '>':
				error_exit("Invalid rules")
			if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][pt2]) > -1:
				arg += 1
			if g[st][pt2] == '(':
				br_o += 1
			if g[st][pt2] == ')':
				br_c += 1
			pt2 += 1
		if br_o != br_c:
			error_exit("Invalid rules")
		if arg < 1:
			error_exit("Invalid rules")
	deep_check(g)

def fact_getter(r):
	ff = {}
	for i in range(len(r)):
		tmp = []
		if(len(r[i][1]) == 1):
			if r[i][1] in ff:
				pass
			else:
				ff[r[i][1]] = [False]
			for a in range(len(r[i][0])):
				tmp.append(r[i][0][a])
			ff[r[i][1]].append(tmp)
			r[i] = '-del'
	return (ff)

def add_false(ff, g):
	for st in range(len(g)):
		for i in range(len(g[st])):
			if is_simbol_in_str("ABCDEFGHIJKLMNOPQRSTUVWXYZ", g[st][i]) > -1:
				if g[st][i] in ff:
					pass
				else:
					ff[g[st][i]] = [False]

def add_facts(f, ff):
	f = f.strip()
	for i in range(len(f)):
		if f[i] in ff:
			ff[f[i]][0] = True
		else:
			ff[f[i]] = [True]

def add_queries(ff, q):
	q = q.strip()
	for i in range(len(q)):
		if q[i] in ff:
			if ff[q[i]][0] != True:
				ff[q[i]][0] = False
		else:
			ff[q[i]] = [False]

def eqer(r):
	re = []
	if len(r) == 0:
		re.append(None)
		return (re)
	for i in range(len(r)):
		re.append([])
		for g in range(2):
			re[i].append([])
			if g == 0:
				re[i].append(None)
	for i in range(len(r)):
		for a in range(len(r[i][1])):
			re[i][0].append(r[i][1][a])
		for a in range(len(r[i][0])):		
			re[i][2].append(r[i][0][a])
	return (re)

def main():
	if (len(sys.argv) == 1):
		error_exit("0 arguments")
	g = read_add_error(sys.argv[1])
	q = parse_queries_and_facts(g, '?')
	f = parse_queries_and_facts(g, "=")
	remover(g)
	check_rule(g)
	r = RPN(g)
	ff = fact_getter(r)
	remover(r)
	Equep = eqer(r)
	add_false(ff, g)
	add_queries(ff, q)
	if q == "" :
		error_exit("Invalid queries")
	add_facts(f, ff)
	mf(ff, Equep)
	final_out(ff, q)

if __name__ == '__main__':
	main()
