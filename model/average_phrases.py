import numpy as np
import nltk
from types import FunctionType

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



if __name__ == '__main__':
    phrases_vec = phrases2vec(['hello','good'])
    print(phrases_vec)
