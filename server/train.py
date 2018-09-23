from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import glob, os
import numpy as np
import random
import sys
import re
import pickle

words = []
word_indices = {}
indices_word = {}

SPECIAL_WORD = "'''KronusIsAwesome'''"
global_data = []

# reads all the training data adn builds a single dictionary of all unique words
# all the data needs to be read once to make a single uniqe dictionary before we create vector
def build_dict(path):

    global words
    global word_indices
    global indices_word
    global SPECIAL_WORD
    global global_data

    os.chdir(path)
    # read one file at a time and add its unique words to dictionary
    for file in glob.glob("*.py"):

        text = open( path+file, 'r').read()

        #TODO: remove all comments from the training data
        #text = re.sub("[\n]", ' ', text)

        #associate words with numbers
        split_data = re.split(' ', text)
        split_data = [s for s in split_data if len(s) >= 1]

        global_data = global_data + split_data
        #remove duplicate words in same file
        new_words = list(set(split_data))
        words = words + new_words

    #remove duplicate words in all global database
    words = list(set(words))
    words.sort()
    words.insert(0,SPECIAL_WORD)

    word_indices = dict((c, i) for i, c in enumerate(words))

    f = open("word_indices.pkl","wb")
    pickle.dump(word_indices,f)
    f.close()

    indices_word = dict((i, c) for i, c in enumerate(words))

    f = open("indices_word.pkl","wb")
    pickle.dump(indices_word,f)
    f.close()


def train_model(path):

    build_dict(path)
    #read data, remove non-alphanumeric chars and convert to lowercase
    """
    text = open(path, 'r').read()

    #TODO: remove all comments from the training data
    #text = re.sub("[^A-Za-z0-9 ]", ' ', text)
    print('corpus length:', len(text))
    
    #associate words with numbers
    split_data = re.split(' ', text)
    split_data = [s for s in split_data if len(s) >= 1]
    words = sorted(list(set(split_data)))
    print('total words:', len(words))
    word_indices = dict((c, i) for i, c in enumerate(words))
        
    f = open("word_indices.pkl","wb")
    pickle.dump(word_indices,f)
    f.close()
    
    indices_word = dict((i, c) for i, c in enumerate(words))
        
    f = open("indices_word.pkl","wb")
    pickle.dump(indices_word,f)
    f.close()

    """
    
    # cut the text into n-grams
    n = 30
    step = 1

    # stores training data as a sliding window size of n
    n_grams = []
    # stores next word which should be predicted
    next_words = []
    for i in range(0, len(global_data) - n, step):
        n_grams.append(global_data[i: i + n])
        next_words.append(global_data[i + n])
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


train_model("/home/ad/Kaggle/CodingAssistant/Kronus/server/TestDir/")


