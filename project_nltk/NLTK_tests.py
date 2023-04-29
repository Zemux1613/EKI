from nltk import CFG, ChartParser, chomsky_normal_form, Production
from nltk.parse.generate import generate


def loadGrammarFromFile(grammar_file):
    with open(grammar_file, 'r') as file:
        return CFG.fromstring(file)


# Hauptprogramm
def main():
    # Pfad zur Grammatikdatei
    grammar_file = 'project_nltk/grammar_cnf.txt'

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
    # if not grammar.is_chomsky_normal_form():
        # note that, the grammar#chomsky_normal_form method can't handle mixed rules like s => asa...
        # grammar = grammar.chomsky_normal_form()
        # grammar = convert_grammar_to_cnf(grammar)
    parser = ChartParser(grammar)
    parse = parser.parse(word)
    for tree in parse:
        tree.pretty_print()
        tree.draw()
        print(f"Height: {tree.height()}")
        print(f"Leaves: {tree.leaves()}")

if __name__ == '__main__':
    main()
