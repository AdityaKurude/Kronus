
# coding: utf-8

# In[1]:


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


# In[ ]:


def generate_similar_text(path):
    
    #read data and convert to lowercase
    data = open(path, 'r').read().lower()
    text = open(path).read().lower()
    print('corpus length:', len(text))
    
    #associate characters with numbers
    chars = sorted(list(set(text)))
    print('total chars:', len(chars))
    print(chars)
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    
    # cut the text in semi-redundant sequences of maxlen characters
    maxlen = 40
    step = 3
    sentences = []
    next_chars = []
    for i in range(0, len(text) - maxlen, step):
        sentences.append(text[i: i + maxlen])
        next_chars.append(text[i + maxlen])
    print('nb sequences:', len(sentences))

    #one hot encoding
    print('Vectorization...')
    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1


    # build the model: a single LSTM
    print('Build model...')
    model = Sequential()
    model.add(LSTM(1024, input_shape=(maxlen, len(chars))))
    model.add(Dense(len(chars)))
    model.add(Activation('softmax'))

    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)


    def sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    # train the model, output generated text after each iteration
    for iteration in range(1, 60):
        print()
        print('-' * 50)
        print('Iteration', iteration)
        model.fit(x, y,
                  batch_size=128,
                  epochs=100)

        start_index = random.randint(0, len(text) - maxlen - 1)

        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print()
            print('----- diversity:', diversity)

            generated = ''
            sentence = text[start_index: start_index + maxlen]
            generated += sentence
            
            print('----- Generating with seed: "' + sentence + '"')
            sys.stdout.write(generated)

            for i in range(400):
                x_pred = np.zeros((1, maxlen, len(chars)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, char_indices[char]] = 1.

                preds = model.predict(x_pred, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_char = indices_char[next_index]

                generated += next_char
                sentence = sentence[1:] + next_char

                sys.stdout.write(next_char)
                sys.stdout.flush()
            print()


# In[ ]:


#generate_similar_text('service_impl.txt')


# In[2]:


def generate_fake_news(path):
    
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
    indices_word = dict((i, c) for i, c in enumerate(words))
    
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


    def sample(preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    # train the model, output generated text after each iteration
    for iteration in range(1, 60):
        print()
        print('-' * 50)
        print('Iteration', iteration)
        model.fit(x, y,
                  batch_size=128,
                  epochs=100)

        start_index = random.randint(0, len(split_data) - n - 1)

        for diversity in [0.2, 0.5, 1.0, 1.2]:
            print()
            print('----- diversity:', diversity)

            generated = ""
            n_gram = " ".join(split_data[start_index : start_index + n])
            generated += n_gram

            for i in range(10):
                x_pred = np.zeros((1, n, len(words)))
                for t, word in enumerate(n_gram.split(" ")):
                    x_pred[0, t, word_indices[word]] = 1.

                preds = model.predict(x_pred, verbose=0)[0]
                next_index = sample(preds, diversity)
                next_word = indices_word[next_index]

                generated += " " + next_word
                n_gram = " ".join(n_gram.split(" ")[1:]) + " " + next_word
              
            	print(generated)


# In[3]:


generate_fake_news('service_impl.txt')


# In[ ]:


generate_similar_text('dna.txt')

