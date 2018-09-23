from __future__ import print_function
from keras.models import load_model

import numpy as np
import re
import pickle


def generate_fake_news(path):
    def manhattan_to_index(l):
        for i in len(l):
            if l[i] == 1:
                return i

    word_indices = pickle.load(open("word_indices.pkl", "rb"))
    indices_word = pickle.load(open("indices_word.pkl", "rb"))
    n = 3
    input = "n_grams def def"
    split_input = re.split(' ', input)
    # next line: possible bs
    split_input = [s for s in split_input if len(s) >= 1]
    split_indices = [word_indices[s] for s in split_input]


    len_network_indices = len(word_indices) if len(word_indices) < n else n

    input_manhattan = np.zeros((1, n, len(word_indices)), np.bool)

    for i in range(len(split_input)):
   	print('i: ', i,' , i + (n - len_network_indices):', (i + (n - len_network_indices)))
        input_manhattan[0][i + (n - len_network_indices)][word_indices[split_input[i]]] = True

    model = load_model('Kronos_V0.h5')
    pred_manhattan = model.predict(input_manhattan)
    print(pred_manhattan)
    pred_word = indices_word[np.argmax(pred_manhattan)]

    # Printing Prediction word for the input
    print(pred_word)


generate_fake_news('/Users/PedroFigueiredo/Desktop/test.txt')
