import spacy
from nltk.corpus import stopwords


def get_spacy_nlp():
    """

    :return: spacy
    """
    nlp = spacy.load("en_core_web_sm")
    return nlp


def get_text_without_stopwords(sentence):
    stopwords_spacy = get_spacy_nlp().Defaults.stop_words

    stop_words = set(stopwords_spacy)
    filtered_sentence = [w for w in sentence.lower().split() if w not in stop_words]
    filtered_sentence = " ".join(filtered_sentence)
    return filtered_sentence


def get_text_without_stopwords_nltk(sentence, language='english'):
    stop_words = set(stopwords.words(language))
    filtered_sentence = [w for w in sentence.lower().split() if w not in stop_words]
    filtered_sentence = " ".join(filtered_sentence)
    return filtered_sentence
