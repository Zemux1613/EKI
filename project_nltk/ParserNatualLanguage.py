import nltk
from nltk import CFG, ChartParser, RecursiveDescentParser
from grammar.grammarTool_03 import *
from project_spacy.PosTagger import *


def loadGrammarFromFile(grammar_file):
    return CFG.fromstring(GrammarTool.read_grammar_from_file(GrammarTool(), grammar_file))


def check_sentence(sentence, grammar):
    parser = RecursiveDescentParser(grammar)
    #words = nltk.word_tokenize(sentence)
    try:
        for tree in parser.parse(sentence):
            print("Zugehörige Syntaxbaumstruktur:", tree)
            return True
        return False
    except ValueError:
        print("Keine Übereinstimmung mit der definierten Grammatik gefunden.")
        return False

# Hauptprogramm
if __name__ == '__main__':
    # Pfad zur Grammatikdatei
    grammar_file = '../grammar/germanQuestions.txt'

    # Lade Grammatikdatei
    grammar = loadGrammarFromFile(grammar_file)

    print(grammar)

    running = True

    print("Type 'cancel' to exit this programm.")

    while (running):
        inputLine = input("Eingabe: ")
        # inputLine = "spielt Tom?"
        if "cancel" in inputLine:
            running = False
            print("Thanks for using me!")
        else:
            #parser = ChartParser(grammar)
            print(f"test for word: '{inputLine}'")
            posTags = PosTagger.getPosTaggs(PosTagger(), inputLine)

            print(posTags)

            # Testen des Parsers
            is_valid = check_sentence(' '.join(posTags), grammar)


            print(f"The word '{inputLine}' is valid: {is_valid}")


