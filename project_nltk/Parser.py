from nltk import CFG, ChartParser
from grammar.grammarTool_03 import *

def loadGrammarFromFile(grammar_file):
    return CFG.fromstring(GrammarTool.read_grammar_from_file(GrammarTool(), grammar_file))


# Hauptprogramm
if __name__ == '__main__':
    # Pfad zur Grammatikdatei
    grammar_file = '../grammar/grammar.txt'

    # Lade Grammatikdatei
    grammar = loadGrammarFromFile(grammar_file)

    print(grammar)

    running = True

    while(running):
        inputLine = input("Eingabe:")
        if "cancel" in inputLine:
            running = False
            print("Thanks for using me!")
        else:
            parser = ChartParser(grammar)
            print(f"test for word: '{inputLine}'")

            try:
                parses = parser.parse(inputLine)
                is_valid = any(parse for parse in parses)
            except ValueError:
                is_valid = False

            print(f"The word '{inputLine}' is valid: {is_valid}")