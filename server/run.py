from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
from keras.models import load_model

import numpy as np
import random
import sys
import re
import pickle

def generate_fake_news(path):

    # #read data, remove non-alphanumeric chars and convert to lowercase
    # text = open(path).read()
    # print('corpus length:', len(text))
    #
    # #associate words with numbers
    # split_data = re.split(' ', text)
    # split_data = [s for s in split_data if len(s) >= 1]
    # words = sorted(list(set(split_data)))
    # print('total words:', len(words))
    # # word_indices = dict((c, i) for i, c in enumerate(words))
    # # indices_word = dict((i, c) for i, c in enumerate(words))


    word_indices = pickle.load(open("word_indices.pkl", "rb"))
    #
    # # cut the text into n-grams
    # n = 3
    # step = 1
    # n_grams = []
    # next_words = []
    # for i in range(0, len(split_data) - n, step):
    #     n_grams.append(split_data[i: i + n])
    #     next_words.append(split_data[i + n])
    # print('nb sequences:', len(n_grams))
    #
    # #one hot encoding
    # print('Vectorization...')
    # x = np.zeros((len(n_grams), n, len(words)), dtype=np.bool)
    # y = np.zeros((len(n_grams), len(words)), dtype=np.bool)
    # for i, n_gram in enumerate(n_grams):
    #     for t, word in enumerate(n_gram):
    #         x[i, t, word_indices[word]] = 1
    #     y[i, word_indices[next_words[i]]] = 1


    # def sample(preds, temperature=1.0):
    #     # helper function to sample an index from a probability array
    #     preds = np.asarray(preds).astype('float64')
    #     preds = np.log(preds) / temperature
    #     exp_preds = np.exp(preds)
    #     preds = exp_preds / np.sum(exp_preds)
    #     probas = np.random.multinomial(1, preds, 1)
    #     return np.argmax(probas)

    input = "print"
    split_input = re.split(' ', input)
    # next line: possible bs
    split_input = [s for s in split_input if len(s) >= 1]
    split_indices = [word_indices[s] for s in split_input]

    model = load_model('Kronos_V0.h5')
    len_split_indices = len(split_indices)
    input_model = np.zeros((len_split_indices, len_split_indices), np.bool)
    for i in range(len_split_indices):
        input_model[i][split_indices] = True

    pred = model.predict(input_model)

generate_fake_news('/Users/PedroFigueiredo/Desktop/test.txt')


