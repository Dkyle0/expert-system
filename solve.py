# # https://pythonist.ru/kopirovanie-obektov-v-python/

ValueFacts = 0
UndefFact = "Undefined"

# Facts = dict()
EqupmentsRulls = dict()

def	RuleAnd(Value0, Value1):
	return Value0 and Value1

def	RuleNot(Value0):
	return not Value0

def	RuleOr(Value0, Value1):
	return Value0 or Value1

def	RuleXor(Value0, Value1):
	return (Value0 and not Value1) or (Value1 and not Value0)

# def FillGraf(Facts):
# 	Facts["A"] = [None]
# 	Facts["B"] = [None]
# 	Facts["C"] = [None]
# 	Rulls = ["A", "B", "+"]
# 	Facts["C"].append(Rulls)
# 	Facts["A"][ValueFacts] = True
# 	Facts["B"][ValueFacts] = False

def	RuleIsSolve(Rule, Facts):
	allowedSymbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	if type(Rule) == str:
		if Rule in Facts.keys and Facts[Rule] == None:
			return False
	elif type(Rule) == list:
		for i in range(len(Rule)):
			if (type(Rule[i]) == str and Rule[i] in Facts and allowedSymbols.find(Rule[i]) > -1 and Facts[Rule[i]]) == None:
				return False
	return True

def SolveRule(Rule, Facts, field = list()):
	print(Facts)
	while len(Rule) > 0:
		elem = Rule.pop(0)

		if elem == "+":
			Value1 = field.pop()
			Value0 = field.pop()
			field.append(RuleAnd(Value0, Value1))

		elif elem == "!":
			Value0 = field.pop()
			field.append(RuleNot(Value0))

		elif elem == "|":
			Value1 = field.pop()
			Value0 = field.pop()
			field.append(RuleOr(Value0, Value1))

		elif elem == "^":
			Value1 = field.pop()
			Value0 = field.pop()
			field.append(RuleXor(Value0, Value1))
		
		elif elem in Facts.keys():
			if Facts[elem][ValueFacts] == UndefFact:
				field1 = field.copy
				field1.append(True)
				Result1 = SolveRule(Rule.copy, field1)
				field2 = field.copy
				field2.append(False)
				Result2 = SolveRule(Rule.copy, field2)

				if Result1 == Result2:
					return Result1
				elif type(Result1) == str or type(Result2) == str:
					return UndefFact
				elif Result1 == None or Result2 == None:
					return None

			else:
				field.append(Facts[elem][ValueFacts])
		
		else:
			print("Error", elem)
			break
	if len(field) == 1:
		return (field.pop())
	return None

def mf(Facts):
	# FillGraf(Facts)
	# print (F)
	# print (Facts)
	proc = True
	while proc == True:
		proc = False
		for NameFact in Facts.keys():
			if Facts[NameFact][ValueFacts] == None and len(Facts[NameFact]) > 1:
				for index in range(1,len(Facts[NameFact])):
					Rule = Facts[NameFact][index]
					print(Rule)
					if RuleIsSolve(Rule, Facts):
						proc = True
						Solve = SolveRule(Rule.copy(), Facts)
						if Facts[NameFact][ValueFacts] == None:
							Facts[NameFact][ValueFacts] = Solve
						elif Facts[NameFact][ValueFacts] != Solve:
							Facts[NameFact][ValueFacts] = UndefFact
	print(Facts)
