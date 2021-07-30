import re

import wikipedia as wiki
import wikipedia.exceptions
from translate import Translator

from jarvis.utils import languages_utils, fake_emails_generator


def page_summary(query, auto_suggest=True):
    """Request the summary for the result.
    writes in inverted-pyramid style, so the first sentence is the
    most important, the second less important, etc.  Two sentences
    is all we ever need.
    Arguments:
        wiki result (str): Wikipedia match name
        auto_suggest (bool): True if auto suggest was used to get this
                             result.
    """

    print(query)
    lines = 2
    wiki.set_lang(languages_utils.get_language_only_country())

    # First try in local language
    try:
        summary = wiki.summary(title=query, sentences=lines, auto_suggest=auto_suggest)
    except wikipedia.exceptions.WikipediaException:
        try:
            # Second try if nothing is found in the local language, try in english and translate the answer
            summary = summary_english_translated(query)
        except wikipedia.exceptions.WikipediaException:
            return "Found nothing"

    if "==" in summary or len(summary) > 250:
        # We hit the end of the article summary or hit a really long
        # one.  Reduce to first line.
        summary = summary.split('. ')[0]

    # replace inc. by incorporation (for pronunciation)
    summary = summary.replace("Inc.", "Incorporation")

    # Clean text to make it more speakable
    return re.sub(r'\([^)]*\)|/[^/]*/', '', summary)


def summary_english_translated(query):
    wiki.set_lang("en")
    summary = wiki.page(title=query, auto_suggest=False).summary
    summary = re.sub(r'\([^)]*\)|/[^/]*/', '', str(summary))
    summary = summary.split('. ')[0] + summary.split('. ')[1]

    translator = Translator(to_lang=languages_utils.get_language_only_country(), from_lang="en",
                            email=fake_emails_generator.generate_random_email())
    summary = translator.translate(summary)
    return summary
