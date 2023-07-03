from nltk import CFG, ChartParser
from nltk.parse.generate import generate

if __name__ == '__main__':
    IFGrammar = CFG.fromstring("""Start -> 'if(exp){' N1 '}' 
                                N1    -> 'statement' | Start 
                             """)

    IfElseGrammar = CFG.fromstring("""Start -> 'if(exp){' N1 '}else{' N1 '}' |'if(exp){' N1 '}'  
                                N1    -> 'statement' | Start 
                             """)
    IfElseIfElseGrammar = CFG.fromstring("""Start -> 'if(exp){' N1 '}' N2  
                                N1    -> 'statement' | Start 
                                N2 -> '' | 'else' Start | 'else {' N1 '}'
                             """)

    grammarInUse = IfElseGrammar

    print(grammarInUse)

    for item in list(generate(grammarInUse, depth=6)):
        parser = ChartParser(grammarInUse)
        parse = parser.parse(item)
        for tree in parse:
            tree.pretty_print()
            tree.draw()
            print(f"Height: {tree.height()}")
            print(f"Leaves: {tree.leaves()}")
