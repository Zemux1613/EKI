def getContent(filename):
    content = ""
    with open(filename, "r") as file:
        for line in file:
            if not line.endswith(";"):
                content += line + ";"
            else:
                content += line
    return content

nonTerminalIndex = 0

def generateNonTerminal():
    global nonTerminalIndex
    nonTerminalIndex = nonTerminalIndex + 1


def replaceSyntax(x):
    if x.__contains__("?"):
        x = x.replace("?", " | epsilon")

    if x.__contains__("+"):
        nonTerminal = "A" + str(nonTerminalIndex)
        generateNonTerminal()
        x = x.replace("+", "")
        content = x.strip()
        x = nonTerminal + "\n"
        x += nonTerminal + " -> " + content + " | " + nonTerminal + content

    if x.__contains__("*"):
        nonTerminal = "A" + str(nonTerminalIndex)
        generateNonTerminal()
        x = x.replace("*", "")
        content = x.strip()
        x = nonTerminal + "\n"
        x += nonTerminal + " -> " + content + " | " + nonTerminal + content + " | epsilon"

    return x.strip()

if __name__ == '__main__':
    content = getContent("test_grammar.txt")
    for line in content.split(";"):
        rhs = line.split("->")[0].strip()
        if line.__contains__("|"):
            split = line.split("|")
            for x in split:
                currentLhs = x
                if currentLhs.__contains__("->"):
                    currentLhs = x.split("->")[1].strip()
                lhs = replaceSyntax(currentLhs)
                print(rhs + " -> " + lhs.strip())
