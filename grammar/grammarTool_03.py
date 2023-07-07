import re


def get_content(filename):
    content = ""
    with open(filename, "r") as file:
        for line in file:
            if not line.endswith(";"):
                content += line + ";"
            else:
                content += line
    return content


nonTerminalIndex = 0


def generate_non_terminal():
    global nonTerminalIndex
    nonTerminalIndex = nonTerminalIndex + 1
    return "A" + str(nonTerminalIndex)


def handle_disjunctions(content):
    new_grammar = []
    for line in content.split(";"):
        if "|" in line:
            if "->" in line:
                lhs = line.split("->")[0]
                rhs = line.split("->")[1]
                for option in rhs.split("|"):
                    new_rule = f"{lhs} -> {option}"
                    new_grammar.append(new_rule)
        else:
            new_grammar.append(line)
    return new_grammar


finalRules = []


def read_grammar_from_file(filename, debug=False):
    content = get_content(filename)

    if debug:
        print(f"origin grammar:\n{content}")
    #
    # handle disjunctions
    #
    contentWithoutDisjunctions = handle_disjunctions(content)

    #
    # Search for scopes
    #
    rulesWithScope = []
    rulesWithoutScope = []
    for rule in contentWithoutDisjunctions:
        if "(" in rule or ")" in rule:
            rulesWithScope.append(rule)
            if debug:
                print("with scope: " + rule)
        else:
            rulesWithoutScope.append(rule)
            if debug:
                print("without scope: " + rule)

    #
    # handle syntax features
    #
    global finalRules

    for rule in rulesWithScope:
        if "*" in rule or "?" in rule or "+" in rule:
            if "?" in rule:
                handle_expression_rule(rule, '?')
            if "+" in rule:
                handle_expression_rule(rule, '+')
            if "*" in rule:
                handle_expression_rule(rule, '*')

    for rule in rulesWithoutScope:
        if "?" in rule or "+" in rule or "*" in rule:
            if "?" in rule:
                handle_single_rule(rule, '?')
            if "+" in rule:
                handle_single_rule(rule, '+')
            if "*" in rule:
                handle_single_rule(rule, '*')
        else:
            finalRules.append(rule)

    if debug:
        print("Grammar: ")
        for rule in finalRules:
            print(rule)


def handle_expression_rule(rule, symbol):
    pattern = r"\(([^)]*)\)" + re.escape(symbol)
    lhs, rhs = rule.split("->")
    matches = re.findall(pattern, rhs)
    if matches:
        for match in matches:
            print("rhs begin: " + rhs)
            non_terminal = generate_non_terminal()
            expression = match
            new_rule = get_helper_rule(expression, non_terminal, symbol)
            rhs = rhs.replace("(" + expression + ")" + symbol, f" {non_terminal} ")
            print("rhs after: " + rhs)
            finalRules.append(new_rule)
        finalRules.append(f"{lhs} -> {rhs}")
        print("Cleaned: " + lhs + " -> " + rhs)


def get_helper_rule(expression, nonTerminal, symbol):
    if symbol == "?":
        new_rule = f"{nonTerminal} -> {expression} | ''"
    elif symbol == "+":
        new_rule = f"{nonTerminal} -> {expression} | {nonTerminal} {expression}"
    elif symbol == "*":
        new_rule = f"{nonTerminal} -> '' | {nonTerminal} {expression}"
    return new_rule


def handle_single_rule(rule, symbol):
    lhs, rhs = rule.split("->")
    matches = re.findall(r"(\'.\'|.)" + re.escape(symbol), rhs)
    for match in matches:
        if match:
            single_char = match
            non_terminal = generate_non_terminal()
            new_rule = get_helper_rule(single_char, non_terminal, symbol)
            rhs = rhs.replace(single_char, f" {non_terminal} ")
            finalRules.append(new_rule)

    finalRules.append(f"{lhs} -> {rhs.replace(symbol, '')}")

if __name__ == '__main__':
   read_grammar_from_file("grammar.txt", True)