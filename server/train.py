from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
import re
import pickle

def train_model(path):

    #read data, remove non-alphanumeric chars and convert to lowercase
    data = open(path, 'r').read().lower()
    text = open(path).read().lower()
    #text = re.sub("[^A-Za-z0-9 ]", ' ', text)
    print('corpus length:', len(text))
    
    #associate words with numbers
    split_data = re.split(' ', text)
    split_data = [s for s in split_data if len(s) >= 1]
    words = sorted(list(set(split_data)))
    print('total words:', len(words))
    word_indices = dict((c, i) for i, c in enumerate(words))
        
    f = open("word_indices.pkl","wb")
    pickle.dump(indices_word,f)
    f.close()
    
    indices_word = dict((i, c) for i, c in enumerate(words))
        
    f = open("indices_word.pkl","wb")
    pickle.dump(indices_word,f)
    f.close()
    
    # cut the text into n-grams
    n = 3
    step = 1
    n_grams = []
    next_words = []
    for i in range(0, len(split_data) - n, step):
        n_grams.append(split_data[i: i + n])
        next_words.append(split_data[i + n])
    print('nb sequences:', len(n_grams))

    #one hot encoding
    print('Vectorization...')
    x = np.zeros((len(n_grams), n, len(words)), dtype=np.bool)
    y = np.zeros((len(n_grams), len(words)), dtype=np.bool)
    for i, n_gram in enumerate(n_grams):
        for t, word in enumerate(n_gram):
            x[i, t, word_indices[word]] = 1
        y[i, word_indices[next_words[i]]] = 1

    # build the model: a single LSTM
    print('Build model...')
    model = Sequential()
    model.add(LSTM(1024, input_shape=(n, len(words))))
    model.add(Dense(len(words)))
    model.add(Activation('softmax'))

    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    
    # train the model, output generated text after each iteration
    for iteration in range(1, 3):
        print()
        print('-' * 50)
        print('Iteration', iteration)
        model.fit(x, y,
                  batch_size=128,
                  epochs=100)
                  
                  
    model.save('Kronos_V0.h5') 


train_model('service_impl.txt')


