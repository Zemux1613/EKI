from nltk import CFG, ChartParser
from grammar.grammarTool import *
from project_spacy.PosTagger import *

def loadGrammarFromFile(grammar_file):
    fileOutput = GrammarTool.readGrammarFromFile(GrammarTool(), grammar_file)
    return CFG.fromstring(fileOutput)

# Hauptprogramm
if __name__ == '__main__':
    # Pfad zur Grammatikdatei
    grammar_file = '../grammar/smallestSentences.txt'

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
            posTags = str(PosTagger.getPosTaggs(PosTagger(), inputLine))
            word = ""
            for posTag in posTags:
                word += posTag.strip() + " "
            print(word)
            parses = parser.parse(word)
            print(f"The word '{inputLine}' is valid: {any(parse for parse in parses)}")

