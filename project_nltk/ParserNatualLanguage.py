import nltk
from nltk import CFG, ChartParser
from nltk.parse import chart

from grammar.grammarTool_03 import *
from project_spacy.PosTagger import *


def loadGrammarFromFile(grammar_file):
    return CFG.fromstring(GrammarTool.read_grammar_from_file(GrammarTool(), grammar_file))

def check_sentence(sentence, grammar):
    parser = nltk.ChartParser(grammar)
    try:
        for tree in parser.parse(nltk.word_tokenize(sentence)):
            print("Zugehörige Syntaxbaumstruktur:", tree)
            return True
        print("Keine Übereinstimmung mit der definierten Grammatik gefunden.")
        return None
    except ValueError as e:
        print("Fehler beim Parsen:", e)
        return False

# Hauptprogramm
if __name__ == '__main__':

    chart.demo_grammar()

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
            pos_tags = PosTagger.getPosTaggs(PosTagger(), inputLine)

            print(pos_tags)

            # Testen des Parsers
            is_valid = check_sentence(' '.join(pos_tags), grammar)

            print(f"The word '{inputLine}' is valid: {is_valid}")