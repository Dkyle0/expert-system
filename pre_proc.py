from utils import is_simbol_in_str

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