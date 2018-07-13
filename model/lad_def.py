from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

def lda_topicn(word_list, num_topics_intial):
    """
    return the topic N and related words M
    It is used for finding reasonably accurate mixtures of topics within a given document set.
    language support: french, english
    :parameter: word list
    :type: str

    """
    doc_set = word_list
    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]

        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        # add tokens to list
        texts.append(stemmed_tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics_intial, id2word=dictionary, passes=20)

    print(ldamodel.print_topics(num_topics=num_topics_intial, num_words=3))


if __name__ == '__main__':
    doc_a = "is a model on many aspects; totally genuine, generosity with his knowledge, very passionnate, very understanding, sensitive, very easy to talk to, open mind, just to name a few"
    doc_b = "and his team are very collaborative. They receive requests from so many departments in CDPQ but still tackle these professionally and mostly on time. in particular is very detailed-oriented and the work produced by his team is of a high standard."
    doc_set = [doc_a, doc_b]
    num_topics_intial = 2
    lda_topicn(doc_set, num_topics_intial)
