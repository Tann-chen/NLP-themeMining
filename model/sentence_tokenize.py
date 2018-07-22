from nltk import sent_tokenize

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
    print("[INFO] doing sentence tokenize ...")

    lst_sentence = []
    if language == 'english':
        lst_sentence = sent_tokenize(text, language='english')
    elif language == 'french':
        lst_sentence = sent_tokenize(text, language='french')
    else:
        print('ERROR:language inputed is out of support in sentence_tokenize()')

    return lst_sentence
