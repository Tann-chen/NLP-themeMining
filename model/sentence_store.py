from repo import insert

class SentenceStore:
    """ the tool class to index sentences && to save to db when the storing cache reaches maximum"""
    def __init__(self, corpus_id):
        self.corpus_id = corpus_id
        self.sentence_cache = {}
        self.current_doc_id = 0
        self.sentence_index = 0
        self.counter = 0
        self.max_cache = 20

    def push(self, sentence):
        self.sentence_cache[str(self.sentence_index)] = sentence
        self.sentence_index = self.sentence_index + 1
        self.counter = self.counter + 1
        if self.counter == self.max_cache:
            insert_doc = {}
            insert_doc["_id"] = self.corpus_id + '#' + str(self.current_doc_id)
            insert_doc["max_index"] = self.sentence_index - 1
            insert_doc["content"] = self.sentence_cache
            # insert to db
            insert("raw_sentences", insert_doc)
            # update the param
            self.current_doc_id = self.current_doc_id + 1
            self.sentence_cache = {}
            self.counter = 0


    def get_current_sentence_index(self):
        return self.sentence_index - 1


    def close(self):
        if len(self.sentence_cache.keys()) > 0:
            insert_doc = {}
            insert_doc["_id"] = self.corpus_id + '#' + str(self.current_doc_id)
            insert_doc["max_index"] = self.sentence_index - 1
            insert_doc["content"] = self.sentence_cache
            # insert to db
            insert("raw_sentences", insert_doc)

        print("[INFO] the sentence store has been closed.")
