import spacy
from spacy.lang.de.examples import sentences
import spacy.cli

class SpacyPOSTagger:

    def posTag(self, sentence):
        # spacy.cli.download("de_core_news_sm")

        nlp = spacy.load("de_core_news_sm")
        doc = nlp(sentence)
        returnList = []
        for token in doc:
            returnList.append(token.pos_)
        return returnList

    if __name__ == '__main__':
        #spacy.cli.download("de_core_news_sm")

        nlp = spacy.load("de_core_news_sm")
        doc = nlp("Wer hat das Buch geschrieben?")
        print(doc.text)
        for token in doc:
            print(token.text, token.pos_, token.lemma_, token.ent_type_, token.dep_)