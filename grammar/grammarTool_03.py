import re


class GrammarTool:

    def __init__(self):
        self.nonTerminalIndex = 0
        self.symbols = ['?', '+', '*']
        self.finalRules = []

    def get_content(self, filename):
        content = ""
        with open(filename, "r") as file:
            for line in file:
                if not line.endswith(";"):
                    content += line + ";"
                else:
                    content += line
        return content

    def generate_non_terminal(self):
        self.nonTerminalIndex += 1
        return "A" + str(self.nonTerminalIndex)

    def handle_disjunctions(self, content):
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

    def searchForExistingNonTerminal(self, content):
        for line in content:
            if re.search("^(A[0-9]+).*$", line):
                nonTerminal = line.split("->")[0].strip()
                index = int(nonTerminal.replace("A", ""))
                if self.nonTerminalIndex < index:
                    self.nonTerminalIndex = index

    def read_grammar_from_file(self, filename):
        content = self.get_content(filename)

        startSymbol = ""
        if "->" in content:
            startSymbol = content.split("->")[0]

        #
        # handle disjunctions
        #
        content_without_disjunctions = self.handle_disjunctions(content)

        #
        # handle existing "A\d+" rules
        #
        self.searchForExistingNonTerminal(content_without_disjunctions)

        #
        # Search for scopes
        #
        rules_with_scope = []
        rules_without_scope = []
        for rule in content_without_disjunctions:
            if "(" in rule or ")" in rule:
                rules_with_scope.append(rule)
            else:
                rules_without_scope.append(rule)

        #
        # handle syntax features
        #

        for rule in rules_with_scope:
            if any(sym in rule for sym in self.symbols):
                self.handle_expression_rule(rule)

        for rule in rules_without_scope:
            if any(sym in rule for sym in self.symbols):
                self.handle_single_rule(rule)
            else:
                self.finalRules.append(rule)

        #
        # For NLTK, move a product rule of the start symbol to the begin
        #
        index = self.find_index_startswith(self.finalRules, startSymbol)
        self.finalRules[0], self.finalRules[index] = self.finalRules[index], self.finalRules[0]

        # if debug:
        # print("Grammar: ")
        # for rule in self.finalRules:
        #    print(rule)
        return self.finalRules

    def find_index_startswith(self, lst, symbol):
        for index, element in enumerate(lst):
            if element.startswith(symbol):
                return index
        return -1  # Falls kein passendes Element gefunden wurde

    def handle_expression_rule(self, rule):
        for symbol in self.symbols:
            pattern = r"\(([^)]*)\)" + re.escape(symbol)
            lhs, rhs = rule.split("->")
            matches = re.findall(pattern, rhs)
            if matches:
                for match in matches:
                    non_terminal = self.generate_non_terminal()
                    expression = match
                    new_rule = self.get_helper_rule(expression, non_terminal, symbol)
                    rhs = rhs.replace(f"({expression}){symbol}", f" {non_terminal} ")
                    self.finalRules.append(new_rule)

            rule = f"{lhs} -> {rhs}"
        self.finalRules.append(f"{lhs} -> {rhs}")

    def get_helper_rule(self, expression, non_terminal, symbol):
        new_rule = ""
        if symbol == "?":
            new_rule = f"{non_terminal} -> {expression} | ''"
        elif symbol == "+":
            new_rule = f"{non_terminal} -> {expression} | {expression} {non_terminal}"
        elif symbol == "*":
            new_rule = f"{non_terminal} -> {expression} {non_terminal} | ''"
        return new_rule

    def handle_single_rule(self, rule):
        for symbol in self.symbols:
            lhs, rhs = rule.split("->")
            matches = re.findall(r"(\'.\'|.)" + re.escape(symbol), rhs)
            for match in matches:
                if match:
                    single_char = match
                    non_terminal = self.generate_non_terminal()
                    new_rule = self.get_helper_rule(single_char, non_terminal, symbol)
                    rhs = rhs.replace(single_char, f" {non_terminal} ")
                    self.finalRules.append(new_rule)

            rule = f"{lhs} -> {rhs.replace(symbol, '')}"
        self.finalRules.append(f"{lhs} -> {rhs.replace(symbol, '')}")
