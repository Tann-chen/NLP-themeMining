import nltk
from nltk import wordpunct_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk import sent_tokenize
from textblob import TextBlob

IF_DEBUG = True

def language_regonize(text):
    """
    return the language of *text*,
    regonize the language by checking whether stopwords in specific language is included in text or not
    language supported : english, french
    :param text: text that includes only one language
    :type text: str
    """
    if IF_DEBUG:
        print("[INFO] start doing language_regonize")

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
        print("[INFO] finish doing language_regonize")

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
        print("[INFO] start doing sentence_tokenize")

    lst_sentence = []
    if language == 'english':
        lst_sentence = sent_tokenize(text, language='english')
    elif language == 'french':
        lst_sentence = sent_tokenize(text, language='french')
    else:
        print('ERROR:language inputed is out of support in sentence_tokenize()')

    if(IF_DEBUG):
        print("[INFO] finish doing sentence_tokenize")

    return lst_sentence

def indexer(token, sentence_id, index_container):
    """
    here not consider postion and freqence of tokens
    here not consider the memory size(spimi algorith)
    """
    if IF_DEBUG:
        print("[INFO] start doing indexer")

    if token in index_container.keys():
        # not consider position and freqence
        posting_list = index_container[token]
        if sentence_id not in posting_list:
            posting_list.append(sentence_id)
    else:
        new_posting_list = [sentence_id]
        index_container[token] = new_posting_list

    if IF_DEBUG:
        print("[INFO] finish doing indexer")



def phrases_extract(text):
    """
    input text
    return the phrases of text
    :return: phrases
    :type: str
    """
    if IF_DEBUG:
        print("[INFO] start doing phrases_extract")

    blob = TextBlob(text)

    if IF_DEBUG:
        print("[INFO] finish doing phrases_extract")
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


if __name__ == '__main__':
    """
    test function
    """
    test_case = "X and his team are very collaborative. They receive requests from so many departments in CDPQ but still tackle these professionally and mostly on time. X in particular is very detailed-oriented and the work produced by his team is of a high standard. X truly cares about the professional development and satisfaction of those under his supervision. This resonates through the work the team does, as each individual member takes pride in projects, feeling a sense of ownership in the work. He keeps the team informed about all aspects of our work - including the purpose, goals, vision, and recipients - so that each member is able to comprehend the scope of the work and envision the final product we strive to produce. In many projects, after discussing his vision, he gives team members the independence to execute, allowing them to display their own creativity and skillsets, but constantly keeping the team aware of the underlying goal so that the project stays on focus."
    # test language_regonize
    print("----- test language -----")
    print(language_regonize(test_case))

    # test sentence_tokenize
    print("----- test sentence tokenize -----")
    lst_sentence = sentence_tokenize(test_case)
    for s in lst_sentence:
        print(s + "||")

    # test phrases_extract
    print("----- test phrases extract -----")
    phs = phrases_extract(test_case)
    for p in phs:
        print(p + "  ")
    print("[size:" + str(len(phs)) + "]")

    # test indexer
    print("----- test indexer -----")
    index_container = {}
    test_case_1 = ["team", "very", "collaborative"]
    test_case_2 = ["receive", "requests", "departments", "CDPQ", "tackle", "professionally", "time"]
    for t in test_case_1:
        indexer(t, 1, index_container)
    for t in test_case_2:
        indexer(t, 2, index_container)
    print(index_container)
