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


def replaceSyntax(x, rhs):
    replaceRule = ""
    if x.__contains__("?"):
        x = x.replace("?", " | epsilon")

    if x.__contains__("+"):
        nonTerminal = "A" + str(nonTerminalIndex)
        generateNonTerminal()
        x = x.replace("+", "")
        content = x.strip()
        replaceRule = rhs + " -> " + nonTerminal
        x = nonTerminal + " -> " + content + " | " + nonTerminal + content

    if x.__contains__("*"):
        nonTerminal = "A" + str(nonTerminalIndex)
        generateNonTerminal()
        x = x.replace("*", "")
        content = x.strip()
        replaceRule = rhs + " -> " + nonTerminal
        x = nonTerminal + " -> " + content + " | " + nonTerminal + " " + content + " | epsilon"

    return x.strip(), replaceRule

def readGrammarFromFile(filename):
    output = ""
    startSymbol = ""
    content = getContent(filename)
    if content.__contains__("->"):
        startSymbol = content.split("->")[0]

    #
    # Now here are advanced syntax simplifications
    #

    for line in content.split(";"):
        if len(line) == 0:
            continue
        rhs = line.split("->")[0].strip()
        if line.__contains__("|"):
            split = line.split("|")
            for x in split:
                currentLhs = x
                if currentLhs.__contains__("->"):
                    currentLhs = x.split("->")[1].strip()
                lhs, replaceRule = replaceSyntax(currentLhs, rhs)
                # print(rhs + " -> " + lhs.strip())
                output += lhs.strip() + "\n"
                if not len(replaceRule) == 0:
                    output += replaceRule + "\n"
        else:
            currentLhs = line
            if currentLhs.__contains__("->"):
                line.split("->")[1].strip()
            lhs, replaceRule = replaceSyntax(currentLhs, rhs)
            # print(rhs + " -> " + lhs.strip())
            output += lhs.strip() + "\n"
            if not len(replaceRule) == 0:
                output += replaceRule + "\n"

    #
    # For NLTK, move a product rule of the start symbol to the begin
    #
    output_split = output.split("\n")
    output = ""
    index = 0
    for line in output_split:
        if line.startswith(startSymbol):
            output_split[0], output_split[index] = output_split[index], output_split[0]
            break
        index = index + 1

    for line in output_split:
        output += line + "\n"

    return output
