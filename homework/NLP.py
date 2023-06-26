from nltk import CFG, ChartParser
from nltk.parse.generate import generate

if __name__ == '__main__':
    grammarInUse = CFG.fromstring(
        """
        s -> 'Was' verb substantiv1 '?' | 'Was' verb pronom substantiv2 '?'
        verb -> 'ist' | 'kann' | 'bedeutet' | 'verstehst' | 'verbindest' | 'tust' | 'machst' | 'kannst' | 'magst' 
        substantiv1 -> 'ein Auto' | 'eine Mutter sein' | 'Stehen'
        substantiv2 -> 'unter Lernen' | 'mit Essen' | 'mit Schnüren' | 'gern' | 'am liebsten' | 'gut' | 'nicht'
        pronom -> 'Du'
        """
    )

    for item in list(generate(grammarInUse, n=100)):
        parser = ChartParser(grammarInUse)
        parse = parser.parse(item)
        print(f"word:{item}")
        for tree in parse:
            tree.pretty_print()
            #tree.draw()
            print(f"Height: {tree.height()}")
            print(f"Leaves: {tree.leaves()}")
