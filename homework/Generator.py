from nltk import CFG, ChartParser
from nltk.parse.generate import generate
from grammar.grammarTool_03 import *

if __name__ == '__main__':
    grammarInUse = CFG.fromstring("""
    Fragesatz -> WerFrage
    Fragesatz -> WannFrage
    Fragesatz -> JaNeinFrage
    Fragesatz -> SonstigeFrage
    WerFrage -> 'PRON' 'VERB' A1 'PUNCT'
    A2 -> Satzglied A2
    A2 -> ''
    WannFrage -> 'ADV' 'VERB' A2 'PUNCT'
    A3 -> Satzglied A3
    A3 -> ''
    JaNeinFrage -> 'VERB' 'PRON' A3 'PUNCT'
    A4 -> Satzglied A4
    A4 -> ''
    JaNeinFrage -> 'VERB' 'PROPN' A4 'PUNCT'
    A5 -> Satzglied A5
    A5 -> ''
    JaNeinFrage -> 'VERB' 'NOUN' A5 'PUNCT'
    A6 -> Satzglied A6
    A6 -> ''
    SonstigeFrage -> Fragepronomen 'AUX' 'PRON' A6 'PUNCT'
    A1 -> Satzglied A1
    A1 -> ''
    Fragepronomen -> 'PRON'
    Fragepronomen -> 'DET'
    Satzglied -> 'ADJ'
    Satzglied -> 'ADP'
    Satzglied -> 'ADV'
    Satzglied -> 'AUX'
    Satzglied -> 'CCONJ'
    Satzglied -> 'DET'
    Satzglied -> 'INTJ'
    Satzglied -> 'NOUN'
    Satzglied -> 'NUM'
    Satzglied -> 'PART'
    Satzglied -> 'PRON'
    Satzglied -> 'PROPN'
    Satzglied -> 'SCONJ'
    Satzglied -> 'SYM'
    Satzglied -> 'VERB'
    Satzglied -> 'X'
    """)

    print(grammarInUse)

    for item in list(generate(grammarInUse, depth=3)):
        print(item)
        parser = ChartParser(grammarInUse)
        parse = parser.parse(item)
        #print(f"word:{item}")
        for tree in parse:
            #tree.pretty_print()
            #tree.draw()
            #print(f"Height: {tree.height()}")
            print(f"Leaves: {tree.leaves()}")
