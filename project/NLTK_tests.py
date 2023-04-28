from nltk import CFG, ChartParser, chomsky_normal_form, Production
from nltk.parse.generate import generate


def loadGrammarFromFile(grammar_file):
    with open(grammar_file, 'r') as file:
        return CFG.fromstring(file)


# Hauptprogramm
def main():
    # Pfad zur Grammatikdatei
    grammar_file = 'project/grammar_cnf.txt'

    # Lade Grammatikdatei
    grammar = loadGrammarFromFile(grammar_file)

    print(grammar)
    # print("My start symbol: ")
    # print(grammar.start())
    # print("My production rules: ")
    # print(grammar.productions())
    print("Word generation: ")
    # generate ( grammar, startDeep = optional, maxDeep = optional, amountOfWords = optional )
    # important! Infinitely deep recursion always needs a maximum depth otherwise there will be complications
    print(list(generate(grammar, 0, 5)))
    runPalindromTests(grammar, ['a', 'b', 'bab', 'bb', 'aa', 'aba', 'abb', 'abaaabbbabbbaaaba'])


def runPalindromTests(grammar, words):
    parser = ChartParser(grammar)
    for word in words:
        print(f"test for word: '{word}'")
        parses = parser.parse(word)
        generate_syntax_tree(grammar, word)
        print(f"The word '{word}' is valid: {any(parse for parse in parses)}")


def generate_syntax_tree(grammar, word):
    if not grammar.is_chomsky_normal_form():
        # note that, the grammar#chomsky_normal_form method can't handle mixed rules like s => asa...
        # grammar = grammar.chomsky_normal_form()
        grammar = convert_grammar_to_cnf(grammar)
    parser = ChartParser(grammar)
    parse = parser.parse(word)
    for tree in parse:
        tree.pretty_print()
        print(f"Height: {tree.height()}")
        print(f"Leaves: {tree.leaves()}")


def convert_grammar_to_cnf(grammar):
    new_productions = []
    nonterminals = set()

    for production in grammar.productions():
        lhs = production.lhs()
        rhs = production.rhs()

        if len(rhs) <= 2:
            # If the production has 2 or fewer symbols, add it as is
            new_productions.append(production)
        else:
            # Convert the production to CNF format
            intermediate_symbols = []
            remaining_symbols = list(rhs)
            while len(remaining_symbols) > 2:
                # Create new intermediate symbol
                new_symbol = f'X{len(intermediate_symbols) + 1}'
                intermediate_symbols.append(new_symbol)
                nonterminals.add(new_symbol)

                # Create new production with two symbols
                new_production = Production(lhs, remaining_symbols[:2] + [new_symbol])
                new_productions.append(new_production)

                remaining_symbols = [new_symbol] + remaining_symbols[2:]

            # Create the final production with the remaining symbols
            final_production = Production(lhs, remaining_symbols)
            new_productions.append(final_production)

    # Add the original nonterminals to the set
    nonterminals.update(grammar.start().symbol())
    for production in grammar.productions():
        nonterminals.update(production.lhs().symbol())

    # Create the CNF grammar
    cnf_grammar = CFG(grammar.start(), new_productions)
    return cnf_grammar, nonterminals


if __name__ == '__main__':
    main()
