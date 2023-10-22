value_facts = 0
undef_fact = 'Undetermined'
no_solution = None


def rule_and(value0, value1):
    return value0 and value1


def rule_not(value0):
    return not value0


def rule_or(value0, value1):
    return value0 or value1


def rule_xor(value0, value1):
    return (value0 and not value1) or (value1 and not value0)


def solve_rule_with_table(rule: list, facts, field: list, table, counter):
    if type(rule) == str:
        if facts[rule][value_facts] is False:
            return table[rule][counter]
        return facts[rule][value_facts]
    elif type(rule) == list:
        while len(rule) > 0:
            elem = rule.pop(0)

            if elem == "+":
                value1 = field.pop()
                value0 = field.pop()
                field.append(rule_and(value0, value1))

            elif elem == "!":
                value0 = field.pop()
                field.append(rule_not(value0))

            elif elem == "|":
                value1 = field.pop()
                value0 = field.pop()
                field.append(rule_or(value0, value1))

            elif elem == "^":
                value1 = field.pop()
                value0 = field.pop()
                field.append(rule_xor(value0, value1))

            elif elem in facts.keys():
                if elem in table.keys():
                    value = table[elem][counter]
                else:
                    value = facts[elem][value_facts]
                field.append(value)

            else:
                print("Error", elem)
                exit(1)
        if len(field) == 1:
            return field.pop()
    print("Error type", type(rule))
    exit(1)


def solve_rule(rule, facts, field):
    if type(rule) == str:
        return facts[rule][value_facts]

    elif type(rule) == list:
        while len(rule) > 0:
            elem = rule.pop(0)

            if elem == "+":
                value1 = field.pop()
                value0 = field.pop()
                field.append(rule_and(value0, value1))

            elif elem == "!":
                value0 = field.pop()
                field.append(rule_not(value0))

            elif elem == "|":
                value1 = field.pop()
                value0 = field.pop()
                field.append(rule_or(value0, value1))

            elif elem == "^":
                value1 = field.pop()
                value0 = field.pop()
                field.append(rule_xor(value0, value1))

            elif elem in facts.keys():
                field.append(facts[elem][value_facts])

            else:
                print("Error", elem)
                exit(1)
        if len(field) == 1:
            return field.pop()
    print("Error type", type(rule))
    exit(1)


def all_facts_are_true(facts, equpments_ruls):
    for fact in facts.keys():
        if not facts[fact][value_facts]:
            return False

    if equpments_ruls is not None and len(equpments_ruls) > 0 and equpments_ruls[0] is not None:
        for List in equpments_ruls:
            value0 = solve_rule(List[0].copy(), facts, list())
            if value0 != no_solution:
                for rule in List[2::]:
                    value1 = solve_rule(rule.copy(), facts, list())

                    if value0 == no_solution or value1 == no_solution:
                        return False

                    if value0 == undef_fact and value1 != undef_fact:
                        return False

                    elif value1 != undef_fact:
                        if value0 != value1:
                            print("Error", List[0], " != ", rule)
                            exit(1)
            else:
                return False
    return True


def all_facts_and_ruls(table, counter, facts, equpments_ruls, output=False):
    for fact in table.keys():
        if len(facts[fact]) > 1:
            value0 = table[fact][counter]
            for rule in facts[fact][1::]:
                value1 = solve_rule_with_table(rule.copy(), facts, list(), table, counter)
                if value0 != value1:
                    if output:
                        print('For ', fact, ': ', value0, ' and solve of rule ', rule, ' is ', value1)
                    return False

    if equpments_ruls is not None and len(equpments_ruls) > 0 and equpments_ruls[0] is not None:
        for List in equpments_ruls:
            first = True
            for rule in List:
                if type(rule) == list or type(rule) == str:
                    if first:
                        if output:
                            rule0 = rule
                        value0 = solve_rule_with_table(rule.copy(), facts, list(), table, counter)
                        if value0 == no_solution:
                            if output:
                                print('There is no solution for this rule:', rule0)
                            return False
                        first = False

                    else:
                        value1 = solve_rule_with_table(rule.copy(), facts, list(), table, counter)
                        if value1 == no_solution:
                            if output:
                                print('There is no solution for this rule:', rule)
                            return False
                        if value0 != value1:
                            if output:
                                print('For ', rule0, ': ', value0, ' and for ', rule, ': ', value1)
                            return False
                        if value1 == undef_fact:
                            value0 = undef_fact

    return True

def truth_table(facts, equpments_ruls, base=2):
    table = dict()
    length = 0
    for fact in facts.keys():
        if not facts[fact][value_facts] and len(facts[fact]) > 1:
            table[fact] = [None]
            length += 1

    if equpments_ruls is not None and len(equpments_ruls) > 0 and equpments_ruls[0] is not None:
        for List in equpments_ruls:
            rule = List[0]
            for fact in rule:
                if fact in facts.keys() and not facts[fact][value_facts]:
                    if not (fact in table.keys()):
                        table[fact] = [None]
                        length += 1

    i = 1
    for fact in table.keys():
        for counter in range(base ** length):
            if (counter % (base * i)) < i:
                table[fact].append(False)
            else:
                table[fact].append(True)
        i *= base

    first = True
    for counter in range(1, base ** length + 1):

        if first:
            if all_facts_and_ruls(table, counter, facts, equpments_ruls):
                for fact in table.keys():
                    table[fact][value_facts] = table[fact][counter]
                first = False
        else:
            if all_facts_and_ruls(table, counter, facts, equpments_ruls):
                for fact in table.keys():
                    if table[fact][value_facts] != table[fact][counter]:
                        table[fact][value_facts] = undef_fact

    if first:
        print("Error: Illegal rules!")
        exit(1)

    for fact in table.keys():
        facts[fact][value_facts] = table[fact][value_facts]


def is_there_loop(facts, equpments_ruls):
    dependencies = dict()
    for fact in facts.keys():
        dependencies[fact] = set()
        if len(facts[fact]) > 1:
            for rule in facts[fact][1::]:
                if type(rule) == list:
                    for sym in rule:
                        if sym in facts.keys():
                            dependencies[fact].add(sym)
                elif type(rule) == str and rule in facts.keys():
                    dependencies[fact].add(sym)

    if equpments_ruls is not None and len(equpments_ruls) > 0 and equpments_ruls[0] is not None:
        for ruls_list in equpments_ruls:
            if len(ruls_list) > 2:
                rule0 = ruls_list[0]
                for sym0 in rule0:
                    if sym0 in facts.keys():
                        for rule in ruls_list[2::]:
                            if type(rule) == list:
                                for sym in rule:
                                    if sym in facts.keys():
                                        dependencies[sym0].add(sym)
                            elif type(rule) == str and rule in facts.keys():
                                dependencies[sym0].add(rule)

    proc = True
    while proc:
        proc = False
        for fact in dependencies.keys():
            length0 = len(dependencies[fact])
            if length0 > 0:
                for elem in dependencies[fact].copy():
                    dependencies[fact].update(dependencies[elem])
                if len(dependencies[fact]) > length0:
                    proc = True

    for fact in dependencies.keys():
        if fact in dependencies[fact]:
            return True
    return False


def mf(facts, equpments_ruls):

    if is_there_loop(facts, equpments_ruls):
        print('Error: Loop detected!')
        exit(1)
    proc = True
    while proc:
        proc = False
        for name_fact in facts.keys():
            if not facts[name_fact][value_facts] and len(facts[name_fact]) > 1:
                for index in range(1, len(facts[name_fact])):
                    rule = facts[name_fact][index]
                    solve = solve_rule(rule.copy(), facts, list())
                    if solve is True or solve == undef_fact:
                        proc = True
                        facts[name_fact][value_facts] = solve
                        break

    if not all_facts_are_true(facts, equpments_ruls):
        truth_table(facts, equpments_ruls)
