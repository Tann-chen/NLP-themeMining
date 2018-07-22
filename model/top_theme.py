import os
import re
import gc
import sys
import nltk
import string

from types import FunctionType
from sentences_store import SentenceStore
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from french_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
from time import gmtime, strftime
from theme_cluster import calculate_distance

from data import save_pickle
from data import read_pickle
from data import save_txt
from data import read_txt
from data import str_of
from func import pos_word
from repo import insert

from stopwords import en_stopwords, fr_stopwords


IF_DEBUG = False

class TopTheme:
    def __init__(self, corpus_description):
        # dependences
        self.language_regonizer = None
        self.sentence_tokenizer = None
        self.theme_cluster = None
        self.indexer = None
        self.phrase_extractor = None
        self.quantizator = None
        self.phrase_quantizator = None
        # global parameters
        self.corpus_id = None
        self.corpus_info = {}
        self.word_vec_map = {}      # map matching between word and vec
        self.theme_clustered = None      # clustered result

        self.corpus_info["description"] = corpus_description

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

        # corpus info
        corpus_size = 0
        sample_num = 0
        sample_details = []
        self.corpus_id = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
        # tools
        sentence_store = SentenceStore(self.corpus_id)
        en_lemmatizer = WordNetLemmatizer()
        fr_lemmatizer = FrenchLefffLemmatizer()
        punctuations = set(string.punctuation)
        translator = Translator()

        en_inversed_index = {}
        fr_inversed_index = {}

        for file_name in os.listdir(folder_path):
            if not file_name.startswith('.'):   # avoid hidden files
                corpus_size = corpus_size + os.path.getsize(folder_path + '/' + file_name)
                doc = read_txt(folder_path + '/' + file_name)
                print("[INFO] reading and dealing the sample " + file_name + " ...")
                sample_num = sample_num + 1
                sample_details.append(file_name)

                # spilit doc to paragraphs, only support single language in one paragraph
                paragraphs = doc.split('\n')
                for parag in paragraphs:
                    language = self.language_regonizer(parag)
                    # sentence tokenize
                    lst_sentence = self.sentence_tokenizer(parag, language)

                    for sentence in lst_sentence:
                        sentence_store.push(sentence)
                        sentence_index = sentence_store.get_current_sentence_index();

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
                        removed_stopwords = [t for t in word_tokens if t not in en_stopwords and t not in fr_stopwords]
                        # lemmatization & index for words
                        for t in removed_stopwords:
                            if language == 'english':
                                pos_token = pos_word(t)
                                if pos_token is not 0:
                                    token = en_lemmatizer.lemmatize(t, pos=pos_token)
                                    self.indexer(token, sentence_index, en_inversed_index)

                            elif language == 'french':
                                token = fr_lemmatizer.lemmatize(t)
                                self.indexer(token, sentence_index, fr_inversed_index)
                        # index for phrase
                        for t in phrases:
                            if language == 'english':
                                self.indexer(t, sentence_index, en_inversed_index)
                            elif language == 'french':
                                self.indexer(t, sentence_index, fr_inversed_index)

        # persist the index
        path = 'out/'
        save_pickle(en_inversed_index, path + self.corpus_id + '_en.pickle')
        save_pickle(fr_inversed_index, path + self.corpus_id + '_fr.pickle')

        # get all tokens
        en_lst_tokens = list(en_inversed_index.keys())
        fr_lst_tokens = list(fr_inversed_index.keys())
        for t in fr_lst_tokens:
            if t in en_lst_tokens:
                fr_lst_tokens.remove(t)     # rm duplicated token across en & fr

        # release memory
        del en_inversed_index
        del fr_inversed_index
        gc.collect()

        # list of vector(list)
        matrix = []

        # english
        for token in en_lst_tokens:
            if ' '  not in token:   # token is a word
                if IF_DEBUG:
                    print("[DEBUG] " + token + " is a word")

                vector = self.quantizator(token)
                if len(vector) > 0:    # avoid wrong-spelling word & extra-rare word
                    matrix.append(vector)
                    self.word_vec_map[token] = vector
            else:   # token is a phrase
                if IF_DEBUG:
                    print("[DEBUG] " + token + " is a phrase")

                vector = self.phrase_quantizator(token, self.quantizator)
                if vector is not 0:  # avoid wrong-spelling word & extra-rare phrase
                    matrix.append(vector)
                    self.word_vec_map[token] = vector

        # french
        for token in lst_tokens_fr:
            if ' ' not in token:
                if IF_DEBUG:
                    print("[DEBUG] " + token + " is a word")
                # tanslate to engish
                after_trans = translator.translate(token, dest='en')
                vector = self.quantizator(after_trans.text)
                if len(vector) > 0:
                    matrix.append(vector)
                    self.word_vec_map[token] = vector
            else:
                if IF_DEBUG:
                    print("[DEBUG] " + token + " is a phrase")

                after_trans = translator.translate(token, dest='en')
                vector = self.phrase_quantizator(after_trans.text, self.quantizator)
                if vector is not 0:
                    matrix.append(vector)
                    self.word_vec_map[token] = vector

        # theme clustering
        self.theme_clustered = self.theme_cluster(num_cluster, matrix, list(self.word_vec_map.keys()))

        # statistic
        self.corpus_info["create_time"] = self.corpus_id   # use timestamp as corpus_id
        self.corpus_info["last_update_time"] = self.corpus_id
        self.corpus_info["sample_num"] = sample_num
        self.corpus_info["sample_size"] = corpus_size
        self.corpus_info["sample_details"] = sample_details
        self.corpus_info["tokens_num"] = len(en_lst_tokens) + len(fr_lst_tokens)
        self.corpus_info["themes_num"] = len(self.theme_clustered["clusters"])
        self.corpus_info["sentences_num"] = sentence_index + 1
        self.corpus_info["queries_num"] = 0

    def query(self, question):
        punctuations = set(string.punctuation)

        # process query
        language = self.language_regonizer(question)
        question = question.lower()
        removed_punc = ''.join(s for s in question if s not in punctuations)
        removed_digit = re.sub(r'\d+', '', removed_punc)
        word_tokens = nltk.word_tokenize(removed_digit)
        question_removed_stopwords = [t for t in word_tokens if t not in en_stopwords and t not in fr_stopwords]
        question_removed_vec = self.quantizator(question_removed_stopwords)

        # calculate similarity
        similarity_container = []
        word_list = self.theme_clustered['clusters']

        for iquery in range(0, len(question_removed_stopwords)):
            for itheme in range(0, len(word_list)):
                similarity = 0
                for w in word_list[itheme]:
                    temp = calculate_distance(self.word_vec_map.get(w), question_removed_vec[iquery])
                    similarity = similarity + temp
                mean_similarity = similarity / len(word_list[itheme])
                entry = []
                entry.append(itheme)
                entry.append(iquery)
                entry.append(mean_similarity)
                similarity_container.append(entry)

        if IF_DEBUG:
            print("\n[DEBUG] --- The similarity between query and corpus clusters --- \n")
            print(similarity_container)
            print("\n")

        # save query info to db
        docu = {}
        docu["_id"] = self.corpus_id + '#' + self.corpus_info["queries_num"]
        docu["corpus_id"] = self.corpus_id
        docu["question"] = question
        docu["query_tokens"] = question_removed_stopwords
        docu["themes"] = self.theme_clustered['representative']
        docu["similarity"] = similarity_container
        insert("queries",docu)

        self.corpus_info["queries_num"] = self.corpus_info["queries_num"] + 1
        print("[INFO] saving query infos to DB successfully.")

    def __del__(self):
        insert("corpus", self.corpus_info)
        print("[INFO] saving corpus infos to DB successfully.")
