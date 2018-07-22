import nltk
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords

def language_regonize(text):
    """
    return the language of *text*,
    regonize the language by checking whether stopwords in specific language is included in text or not
    language supported : english, french
    :param text: text that includes only one language
    :type text: str
    """
    print("[INFO] doing language_regonize ...")
    lang_freq = {}
    support_language = ['english', 'french']
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]
    for lang in support_language:
        stopwords_set = set(stopwords.words(lang))
        words_set = set(words)
        common_ele = words_set.intersection(stopwords_set)
        lang_freq[lang] = len(common_ele)

    return max(lang_freq, key=lang_freq.get)
