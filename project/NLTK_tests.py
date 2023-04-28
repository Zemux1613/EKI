from nltk import CFG, ChartParser
from nltk.parse.generate import generate

def loadGrammarFromFile(grammar_file):
    with open(grammar_file, 'r') as file:
        return CFG.fromstring(file)


# Hauptprogramm
def main():
    # Pfad zur Grammatikdatei
    grammar_file = 'grammar.txt'

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
    runPalindromTests(grammar, ['a', '', 'b', 'bb'])


def runPalindromTests(grammar, words):
    parser = ChartParser(grammar)
    for word in words:
        print(f"test for word: '{word}'")
        parses = parser.parse(word)
        print(f"The word '{word}' is valid: {any(parse for parse in parses)}")


if __name__ == '__main__':
    main()