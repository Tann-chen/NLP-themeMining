import nltk
import numpy as np

from nltk import sent_tokenize
from nltk import wordpunct_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from textblob import TextBlob
from types import FunctionType

IF_DEBUG = False

def language_regonize(text):
    """
    return the language of *text*,
    regonize the language by checking whether stopwords in specific language is included in text or not
    language supported : english, french
    :param text: text that includes only one language
    :type text: str
    """
    if IF_DEBUG:
        print("[INFO] start doing language_regonize.")

    lang_freq = {}
    support_language = ['english','french']
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]
    for lang in support_language:
        stopwords_set = set(stopwords.words(lang))
        words_set = set(words)
        common_ele = words_set.intersection(stopwords_set)
        lang_freq[lang] = len(common_ele)

    if IF_DEBUG:
        print("[INFO] finish doing language_regonize.")

    return max(lang_freq, key=lang_freq.get)


def sentence_tokenize(text, language='english'):
    """
    return an array that includes tokenized sentences of *text*,
    use nltk.PunktSentenceTokenizer to tokenize sentence
    language supported : english, french
    :param text: whole paragraphs of single-language text
    :type text: str
    :param language: the language of the text
    :type language: str
    """
    if IF_DEBUG:
        print("[INFO] start doing sentence_tokenize.")

    lst_sentence = []
    if language == 'english':
        lst_sentence = sent_tokenize(text, language='english')
    elif language == 'french':
        lst_sentence = sent_tokenize(text, language='french')
    else:
        print('ERROR:language inputed is out of support in sentence_tokenize()')

    if(IF_DEBUG):
        print("[INFO] finish doing sentence_tokenize.")

    return lst_sentence

def indexer(token, sentence_id, index_container):
    """
    here not consider postion and freqence of tokens
    here not consider the memory size(spimi algorith)
    """
    if IF_DEBUG:
        print("[INFO] start doing indexer.")

    if token in index_container.keys():
        # not consider position and freqence
        posting_list = index_container[token]
        if sentence_id not in posting_list:
            posting_list.append(sentence_id)
    else:
        new_posting_list = [sentence_id]
        index_container[token] = new_posting_list

    if IF_DEBUG:
        print("[INFO] finish doing indexer.")



def phrases_extract(text):
    """
    input text
    return the phrases of text
    :return: phrases
    :type: str
    """
    if IF_DEBUG:
        print("[INFO] start doing phrases_extract.")

    blob = TextBlob(text)

    if IF_DEBUG:
        print("[INFO] finish doing phrases_extract.")
    return blob.noun_phrases


def pos_word(word):
    input_lst = []
    input_lst.append(word)
    part_of_speech = pos_tag(input_lst)[0][1]
    pos = 0
    if part_of_speech.startswith('V'):
        pos = 'v'
    elif part_of_speech.startswith('N'):
        pos = 'n'
    elif part_of_speech is 'ADJ':
        pos = 'a'
    elif part_of_speech is 'ADV':
        pos = 'r'
    else:
        print("[WARNING] pos of the word is not in (v,n,adj,adv)")
    return pos


def phrases2vec(phrase, quantizator_func):
    if not isinstance(quantizator_func, FunctionType):
        print("ERROR: quantizator_func is not a function object")
        return 0

    word_lst = nltk.word_tokenize(phrase)
    vector_lst = []
    for word in word_lst:
        word_vec = quantizator_func(word)
        if len(word_vec) > 0:
            vector_lst.append(word_vec)

    sum_vec = np.sum(vector_lst, axis = 0)
    result = 0

    if len(vector_lst) > 0:
        result = np.divide(sum_vec,len(vector_lst))

    return result


def calculate_distance(word1, word2):
    distance = np.sqrt(np.sum(np.square(word1 - word2)))
    return distance
