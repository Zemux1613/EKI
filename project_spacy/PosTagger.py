import spacy
from spacy.lang.de.examples import sentences
import spacy.cli

# Universal POS tags: https://universaldependencies.org/u/pos/#universal-pos-tags

class PosTagger:
    def getPosTaggs(self, word):
        # spacy.cli.download("de_core_news_sm")

        nlp = spacy.load("de_core_news_sm")
        doc = nlp(word)
        posTags = []
        print(doc.text)
        for token in doc:
            posTags.append(token.pos_)
            #print(token.text, token.pos_, token.lemma_, token.ent_type_, token.dep_)
        return posTags