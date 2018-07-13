import os
import re
import sys
import nltk
import string
from types import FunctionType
from nltk.stem import WordNetLemmatizer
from french_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
from nltk.corpus import stopwords
from googletrans import Translator
from data import save_pickle
from data import read_pickle
from data import save_txt
from data import read_txt
from data import str_of
from func import pos_word
from theme_cluster import calculate_distance
from repo import insert

IF_DEBUG = False
cust_stop_words = ['x', 'quand','a','to']


class TopTheme:

    def __init__(self):
        self.language_regonizer = 0
        self.sentence_tokenizer = 0
        self.theme_cluster = 0
        self.indexer = 0
        self.phrase_extractor = 0
        self.quantizator = 0
        self.phrase_quantizator = 0
        self.word_vec_map = {}      # map matching between word and vec
        self.theme_clustered = None      # clustered result

    def set_language_regonizer(self, language_regonizer):
        self.language_regonizer = language_regonizer

    def set_sentence_tokenizer(self, sentence_tokenizer):
        self.sentence_tokenizer = sentence_tokenizer

    def set_theme_cluster(self, theme_cluster):
        self.theme_cluster = theme_cluster

    def set_indexer(self, indexer):
        self.indexer = indexer

    def set_phrase_extractor(self, phrase_extractor):
        self.phrase_extractor = phrase_extractor

    def set_quantizator(self, quantizator):
        self.quantizator = quantizator

    def set_phrase_quantizator(self, phrase_quantizator):
        self.phrase_quantizator = phrase_quantizator

    def build(self, folder_path, num_cluster):
        if not isinstance(self.language_regonizer, FunctionType):
            print("ERROR: language_regonizer never setted or type error")
            return 0
        if not isinstance(self.sentence_tokenizer, FunctionType):
            print("ERROR: sentence_tokenizer never setted")
            return 0
        if not isinstance(self.theme_cluster, FunctionType):
            print("ERROR: theme_cluster never setted")
            return 0
        if not isinstance(self.indexer, FunctionType):
            print("ERROR: indexer never setted")
            return 0
        if not isinstance(self.phrase_extractor, FunctionType):
            print("ERROR: phrase_extractor never setted")
            return 0
        if not isinstance(self.quantizator, FunctionType):
            print("ERROR: quantizator never setted")
            return 0
        if not isinstance(self.phrase_quantizator, FunctionType):
            print("ERROR: phrase_quantizator never setted")
            return 0

        sentence_index = -1
        sentences_store = []
        inversed_index = {}
        inversed_index_fr = {}
        punctuations = set(string.punctuation)
        lemmatizer = WordNetLemmatizer()
        fr_lemmatizer = FrenchLefffLemmatizer()
        translator = Translator()


        for file_name in os.listdir(folder_path):
            if not file_name.startswith('.'):   #avoid hidden file
                doc = read_txt(folder_path + '/' + file_name)
                print("[INFO] reading " + file_name + " to build model")
                # spilit doc to paragraphs, suppose single language in one paragraph
                paragraphs = doc.split('\n')
                for parag in paragraphs:
                    language = self.language_regonizer(parag)
                    # sentence tokenize
                    lst_sentence = self.sentence_tokenizer(parag, language)
                    # save original sentence to memory
                    for s in lst_sentence:
                        sentences_store.append(s)

                    for sentence in lst_sentence:
                        sentence_index += 1
                        # case fold
                        sentence = sentence.lower()
                        # extract phrases
                        phrases = self.phrase_extractor(sentence)
                        # remove these phrases from sentence
                        for p in phrases:
                            sentence = sentence.replace(p, '')

                        # remove all punctuation
                        removed_punc = ''.join(s for s in sentence if s not in punctuations)
                        # remove all digits
                        removed_digit = re.sub(r'\d+', '', removed_punc)
                        # tokenize
                        word_tokens = nltk.word_tokenize(removed_digit)
                        # filter stop words
                        removed_stopwords = [t for t in word_tokens if t not in stopwords.words("english") and t not in stopwords.words("french") and t not in cust_stop_words]
                        # lemmatization & index for words
                        for t in removed_stopwords:
                            if language == 'english':
                                pos_token = pos_word(t)
                                if pos_token is not 0:
                                    token = lemmatizer.lemmatize(t, pos=pos_token)
                                    self.indexer(token, sentence_index, inversed_index)

                            elif language == 'french':
                                token = fr_lemmatizer.lemmatize(t)
                                self.indexer(token, sentence_index, inversed_index_fr)
                        # index for phrase
                        for t in phrases:
                            if language == 'english':
                                self.indexer(t, sentence_index, inversed_index)
                            elif language == 'french':
                                self.indexer(t, sentence_index, inversed_index_fr)

        # persist the index
        save_pickle(inversed_index, 'out/index_en.pickle')
        save_txt(str_of(inversed_index), 'out/index_en.txt')
        save_pickle(inversed_index_fr, 'out/index_fr.pickle')
        save_txt(str_of(inversed_index_fr), 'out/index_fr.txt')

        sentence_index = 0
        for i in range(0,len(sentences_store)):
            input_sentence={"_id":str(sentence_index)}
            sentence_index = sentence_index + 1
            input_sentence["content"] = sentences_store[i]
            sentences_store[i] = input_sentence
            insert("corpus",sentences_store[i])

        # get all tokens
        lst_tokens = list(inversed_index.keys())
        lst_tokens_fr = list(inversed_index_fr.keys())

        # list of vector(list)
        matrix = []

        # english
        for token in lst_tokens:
            if ' '  not in token:   # token is a word
                if IF_DEBUG:
                    print("[INFO] " + token + "is a word")

                temp_vector = self.quantizator(token)
                if len(temp_vector) > 0:
                    matrix.append(temp_vector)
                    self.word_vec_map[token] = temp_vector
            else:   # token is a phrase
                if IF_DEBUG:
                    print("[INFO] " + token + "is a phrase")

                temp_vector = self.phrase_quantizator(token, self.quantizator)
                if temp_vector is not 0:
                    matrix.append(temp_vector)
                    self.word_vec_map[token] = temp_vector


        for token in lst_tokens_fr:
            if ' ' not in token:
                after_trans = translator.translate(token, dest='en')
                # print(after_trans.text)
                # tanslate to engish after_tran
                temp_vector = self.quantizator(after_trans.text)
                if len(temp_vector) > 0:
                    matrix.append(temp_vector)
                    self.word_vec_map[token] = temp_vector
            else:
                # translate to english
                after_trans = translator.translate(token, dest='en')
                temp_vector = self.phrase_quantizator(after_trans.text, self.quantizator)
                if temp_vector is not 0:
                    matrix.append(temp_vector)
                    self.word_vec_map[token] = temp_vector

        # theme clustering
        self.theme_clustered = self.theme_cluster(num_cluster, matrix, list(self.word_vec_map.keys()))


    def query(self, question):
        punctuations = set(string.punctuation)

        language = self.language_regonizer(question)
        question = question.lower()

        removed_punc = ''.join(s for s in question if s not in punctuations)
        # remove all digits
        removed_digit = re.sub(r'\d+', '', removed_punc)
        word_tokens = nltk.word_tokenize(removed_digit)
        question_removed_stopwords = [t for t in word_tokens if t not in stopwords.words(language)]
        question_removed_vec = self.quantizator(question_removed_stopwords)


        value = []
        output = []
        word_list = self.theme_clustered['clusters']
        similarity_container = []
        for iquery in range(0, len(question_removed_stopwords)):
            for itheme in range(0, len(word_list)):
                similarity = 0
                for w in word_list[itheme]:
                    temp = calculate_distance(self.word_vec_map.get(w),question_removed_vec[iquery])
                    similarity = similarity + temp
                mean_similarity = similarity / len(word_list[itheme])
                entry = []
                entry.append(itheme)
                entry.append(iquery)
                entry.append(mean_similarity)
                similarity_container.append(entry)
        print(similarity_container)

        # repo
        dict_input = {}
        dict_input["question"] = question
        dict_input["query_tokens"] = question_removed_stopwords
        dict_input["themes"] = self.theme_clustered['representative']
        dict_input["similarity"] = similarity_container
        insert("queries",dict_input)
        print("[INFO] Finish input DB")
        return similarity_container
