import re


def getContent(filename):
    content = ""
    with open(filename, "r") as file:
        for line in file:
            if not line.endswith(";"):
                content += line + ";"
            else:
                content += line
    return content


nonTerminalIndex = 0


def generateNonTerminal():
    global nonTerminalIndex
    nonTerminalIndex = nonTerminalIndex + 1
    return "A" + str(nonTerminalIndex)


def handleDisjunctions(content):
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


def handle_single_character_rule(rule, symbol):
    match = re.search(r"(\'.\'|.)" + re.escape(symbol), rule)
    if match:
        singleChar = match.group(1)
        nonTerminal = generateNonTerminal()
        if symbol == "?":
            newRule = f"{nonTerminal} -> {singleChar} | ''"
        elif symbol == "+":
            newRule = f"{nonTerminal} -> {singleChar} | {nonTerminal} {singleChar}"
        elif symbol == "*":
            newRule = f"{nonTerminal} -> '' | {nonTerminal} {singleChar}"
        rule = rule.replace(singleChar, f" {nonTerminal} ")
        finalRules.append(rule.replace(symbol, "").strip())
        finalRules.append(newRule)


def handle_expression_rule(rule, symbol):
    pattern = r"\(([^)]*)\)" + re.escape(symbol)
    matches = re.findall(pattern, rule)
    if matches:
        for match in matches:
            nonTerminal = generateNonTerminal()
            expression = match
            if symbol == "?":
                newRule = f"{nonTerminal} -> {expression} | ''"
            elif symbol == "+":
                newRule = f"{nonTerminal} -> {expression} | {nonTerminal} {expression}"
            elif symbol == "*":
                newRule = f"{nonTerminal} -> '' | {nonTerminal} {expression}"
            rule = rule.replace("(" + expression + ")" + symbol, f" {nonTerminal} ")
            finalRules.append(rule.replace(symbol, "").strip())
            finalRules.append(newRule)


finalRules = []


def readGrammarFromFile(filename):
    content = getContent(filename)

    #
    # handle disjunctions
    #
    contentWithoutDisjunctions = handleDisjunctions(content)

    #
    # Search for scopes
    #
    rulesWithScope = []
    rulesWithoutScope = []
    for rule in contentWithoutDisjunctions:
        if "(" in rule or ")" in rule:
            rulesWithScope.append(rule)
            # print("with scope: " + rule)
        else:
            rulesWithoutScope.append(rule)
            # print("without scope: " + rule)

    #
    # handle syntax features
    #
    global finalRules

    for rule in rulesWithScope:
        if "*" in rule or "?" in rule or "+" in rule:
            if "*" in rule:
                handle_expression_rule(rule, "*")
            if "+" in rule:
                handle_expression_rule(rule, "+")
            if "?" in rule:
                handle_expression_rule(rule, "?")

    for rule in rulesWithoutScope:
        if "?" in rule or "+" in rule or "*" in rule:
            if "?" in rule:
                handle_single_character_rule(rule, "?")
            if "+" in rule:
                handle_single_character_rule(rule, "+")
            if "*" in rule:
                handle_single_character_rule(rule, "*")
        else:
            finalRules.append(rule)

    print("Grammar: ")
    for rule in finalRules:
        print(rule)


if __name__ == '__main__':
    readGrammarFromFile("grammar.txt")
