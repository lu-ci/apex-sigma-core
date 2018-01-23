import subprocess

import markovify
import spacy

try:
    nlp = spacy.load("en")
except IOError:
    subprocess.Popen(['python', '-m', 'spacy', 'download', 'en'], stdout=subprocess.PIPE).communicate()
    nlp = spacy.load("en")


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
