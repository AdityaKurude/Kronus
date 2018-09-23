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
    def manhattan_to_index(l):
        for i in len(l):
            if l[i] == 1:
                return i

    word_indices = pickle.load(open("word_indices.pkl", "rb"))
    n = 30
    input = "print"
    split_input = re.split(' ', input)
    # next line: possible bs
    split_input = [s for s in split_input if len(s) >= 1]
    split_indices = [word_indices[s] for s in split_input]

    model = load_model('Kronos_V0.h5')
    len_split_indices = len(split_indices) if len(split_indices) < n else n

    input_manhattan = np.zeros((len_split_indices, n), np.bool)

    for i in range(len_split_indices):
        input_manhattan[i][split_indices] = True

    # If length of input is smaller than fixed 'n', fill it with zeros.
    # This makes sure that there is always a fixed size for the network to process.
    if len_split_indices < n:
        input_manhattan = np.concatenate(np.zeros((n - len_split_indices, n), np.bool), input_manhattan)

    pred_manhattan = model.predict(input_manhattan)
    pred_word = split_input[manhattan_to_index(pred_manhattan)]

    # Printing Prediction word for the input
    print(pred_word)


generate_fake_news('/Users/PedroFigueiredo/Desktop/test.txt')
