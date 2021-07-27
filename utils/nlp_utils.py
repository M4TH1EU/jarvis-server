from nltk.corpus import stopwords

from utils.languages_utils import get_language_full_name


def get_text_without_stopwords(sentence, language='english'):
    # if the language given is something like en-us, get the full variant (english)
    if '-' in language:
        language = get_language_full_name(language)

    stop_words = set(stopwords.words(language))
    filtered_sentence = [w for w in sentence.lower().split() if w not in stop_words]
    filtered_sentence = " ".join(filtered_sentence)
    return filtered_sentence


if __name__ == '__main__':
    print(get_text_without_stopwords("Hey give me some info about Elon Musk please"))
