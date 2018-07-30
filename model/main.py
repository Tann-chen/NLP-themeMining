from top_theme import TopTheme
from func import indexer
from func import phrases_extract
from func import language_regonize
from func import phrases2vec
from func import sentence_tokenize

from theme_cluster import kmeans
from word2vector import word2vector


if __name__ == '__main__':
    top_theme_obj = TopTheme("this is a test corpus")
    top_theme_obj.set_language_regonizer(language_regonize)
    top_theme_obj.set_sentence_tokenizer(sentence_tokenize)
    top_theme_obj.set_theme_cluster(kmeans)
    top_theme_obj.set_indexer(indexer)
    top_theme_obj.set_phrase_extractor(phrases_extract)
    top_theme_obj.set_quantizator(word2vector)
    top_theme_obj.set_phrase_quantizator(phrases2vec)
    top_theme_obj.build("in", 4, 15)
    top_theme_obj.query("what is the skills of leadership?")
    top_theme_obj.query("what is the most influence to leadership?")
    top_theme_obj.close()
