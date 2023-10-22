import sys

def is_simbol_in_str(st, simbol):
	return (st.find(simbol))

def error_exit(error_msg):
	print("Error: {}".format(error_msg))
	sys.exit()

def final_out(ff, q):
	q = q.strip()
	for i in range(len(q)):
		if q[i] in ff:
			if (ff[q[i]][0] == True):
				print("\033[32m{}: {}\033[0m" .format(q[i], str(ff[q[i]][0])))
			else:
				print("\033[31m{}: {}\033[0m" .format(q[i], str(ff[q[i]][0])))
		else:
			print("\033[31m {}: False\033[0m" .format(q[i]))

def f_in_list(g, st):
	for i in range(len(g)):
		if (type(g[i]) == str and g[i].find(st) > -1):
			return (1)
	return (0)

def remover(g):
	while(f_in_list(g, "-del") == 1):
		g.remove("-del")
