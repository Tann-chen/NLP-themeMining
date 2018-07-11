import nltk
from nltk.corpus import stopwords

def get_postings_by_token(token, en_index, fr_endex):
    postings = en_index.get(token)
    if postings == None: # not in en_index
        postings = fr_index.get(token)
    # regulate output
    if postings == None:
        postings = []
    return postings


def bubble_sort(lst_dict, ref_key):
    for p in range(0, len(lst_dict)-1):
        for i in range(0, len(lst_dict)-1-p):
            if lst_dict[i].get(ref_key) < lst_dict[i+1].get(ref_key):
                temp = lst_dict[i]
                lst_dict[i] = lst_dict[i+1]
                lst_dict[i+1] = temp


def get_ele_by_attr(list, attr_name, target):
    result = None
    for ele in list:
        if ele.get(attr_name) == target:
            result = ele
            break
    return result


def get_theme_by_token(token, dict_theme):
    target_theme = None
    for theme, lst_tokens in lst_theme:
        if token in lst_tokens:
            target_theme = theme
            break
    return target_theme


def tokenize_query(query):
    query_sentence = query.lower()
    removed_punc = ''.join(s for s in query_sentence if s not in punctuations)
    removed_digit = re.sub(r'\d+', '', removed_punc)
    words = nltk.word_tokenize(removed_digit)
    # language regonize
    lang_freq = {}
    support_language = ['english','french']
    for lang in support_language:
        stopwords_set = set(stopwords.words(lang))
        words_set = set(words)
        common_ele = words_set.intersection(stopwords_set)
        lang_freq[lang] = len(common_ele)

    language = max(lang_freq, key=lang_freq.get)
    tokens = [t for t in words if t not in stopwords.words(language)]
    
    return tokens
