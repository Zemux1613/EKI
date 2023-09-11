from nltk import CFG, ChartParser
from nltk.parse.generate import generate

if __name__ == '__main__':
    grammarInUse = CFG.fromstring(
        """
        s -> 'a' | 'b' | n1 n2 | s n4
        n1 -> '['
        n3 -> ']'
        n2 -> s n3
        n4 -> n5 s
        n5 -> '+'
        """
    )

#    for item in list(generate(grammarInUse, n=1000)):
    parser = ChartParser(grammarInUse)
    parse = parser.parse('[a+[a+b]]')
    #print(f"word:{item}")
    for tree in parse:
        #tree.pretty_print()
        tree.draw()
        #print(f"Height: {tree.height()}")
        print(f"Leaves: {tree.leaves()}")
