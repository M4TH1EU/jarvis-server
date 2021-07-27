import spacy

from jarvis.utils import languages_utils

nlp = None


def get_spacy_nlp():
    global nlp

    if nlp is None:
        print("A Spacy model is starting, it might take a few seconds (starts only once)")
        nlp = spacy.load(languages_utils.get_spacy_model())
    return nlp


def get_text_without_stopwords(sentence):
    stopwords_spacy = get_spacy_nlp().Defaults.stop_words

    stop_words = set(stopwords_spacy)
    filtered_sentence = [w for w in sentence.lower().split() if w not in stop_words]
    filtered_sentence = " ".join(filtered_sentence)
    return filtered_sentence
