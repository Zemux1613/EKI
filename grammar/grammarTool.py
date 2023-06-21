import re


class GrammarTool:
    nonTerminalIndex = 0

    def getContent(self, filename):
        content = ""
        with open(filename, "r") as file:
            for line in file:
                if not line.endswith(";"):
                    content += line + ";"
                else:
                    content += line
        return content

    def generateNonTerminal(self):
        self.nonTerminalIndex = self.nonTerminalIndex + 1
        return "A" + str(self.nonTerminalIndex)

    def searchForExistingNonTerminal(self, content):
        for line in content.split(";"):
            if re.search("^(A[0-9]+).*$", line):
                print("found " + line)
                nonTerminal = line.split("->")[0].strip()
                index = int(nonTerminal.replace("A", ""));
                if self.nonTerminalIndex < index:
                    print("new index " + str(index))
                    self.nonTerminalIndex = index

    def replaceSyntax(self, x, rhs):
        replaceRule = ""
        if "?" in x:
            x = x.replace("?", " | ''")

        if "+" in x:
            nonTerminal = self.generateNonTerminal()
            x = x.replace("+", "")
            content = x.strip()
            replaceRule = rhs + " -> " + nonTerminal
            x = nonTerminal + " -> " + content + " | " + nonTerminal + " " + content

        if "*" in x:
            nonTerminal = self.generateNonTerminal()
            x = x.replace("*", "")
            content = x.strip()
            replaceRule = rhs + " -> " + nonTerminal
            x = nonTerminal + " -> " + content + " | " + nonTerminal + " " + content + " | ''"

        return x.strip(), replaceRule

    def readGrammarFromFile(self, filename):
        output = ""
        startSymbol = ""
        content = self.getContent(filename)
        if "->" in content:
            startSymbol = content.split("->")[0]

        #
        # Now here are advanced syntax simplifications
        #

        self.searchForExistingNonTerminal(content)

        for line in content.split(";"):
            if len(line) == 0:
                continue
            rhs = line.split("->")[0].strip()
            if "|" in line:
                split = line.split("|")
                for x in split:
                    currentLhs = x
                    if "->" in currentLhs:
                        currentLhs = x.split("->")[1].strip()
                    lhs, replaceRule = self.replaceSyntax(currentLhs, rhs)
                    # print(rhs + " -> " + lhs.strip())
                    output += lhs.strip() + "\n"
                    if not len(replaceRule) == 0:
                        output += replaceRule + "\n"
            else:
                currentLhs = line
                if "->" in currentLhs:
                    line.split("->")[1].strip()
                lhs, replaceRule = self.replaceSyntax(currentLhs, rhs)
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
