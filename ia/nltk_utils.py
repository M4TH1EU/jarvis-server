import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer

from utils import languages_utils

stemmer = PorterStemmer()


# TODO : have a look to replace nltk by spacy or the other way (use only one of them)

def tokenize(sentence):
    """
    split sentence into array of words/tokens
    a token can be a word or punctuation character, or number
    """
    # English, Danish, Estonian, French, Greek, Norwegian, Portuguese, Spanish, Turkish,
    # Czech, Dutch, Finnish, German, Italian, Polish, Slovene, and Swedish

    return nltk.word_tokenize(sentence,
                              language=languages_utils.get_language_full_name())


def stem(word):
    """
    stemming = find the root form of the word
    examples:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, words):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype='float32')
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1

    return bag
