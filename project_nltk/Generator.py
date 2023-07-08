from nltk import CFG, Nonterminal
from nltk.parse.generate import generate
from grammar.grammarTool_03 import *

def loadGrammarFromFile(grammar_file):
    return CFG.fromstring(GrammarTool.read_grammar_from_file(GrammarTool(), grammar_file))

# Hauptprogramm
if __name__ == '__main__':
    # Pfad zur Grammatikdatei
    grammar_file = input("Unter welchen Filepath finde ich einen Grammatik-File?: ")
    #grammar_file = '../grammar/sentences_01.txt'

    # Lade Grammatikdatei
    grammar = loadGrammarFromFile(grammar_file)

    print(grammar)

    running = True

    while(running):
        start_symbol = input("Startsymbol: ")
        if "cancel" in start_symbol:
            running = False
            print("Thanks for using me!")
        else:
            print(list(generate(CFG(start=Nonterminal(start_symbol), productions=grammar.productions()), depth=3)))