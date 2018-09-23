import glob, os
import re
import numpy as np
import random
import sys

BASE_PATH = "/home/ad/Kaggle/CodingAssistant/Kronus/server/TestDir/"

os.chdir(BASE_PATH)

words = []

for file in glob.glob("*.py"):

    text = open( BASE_PATH+file, 'r').read()

    #TODO: remove all comments from the training data
    text = re.sub("[\n]", ' ', text)

    #associate words with numbers
    split_data = re.split(' ', text)
    split_data = [s for s in split_data if len(s) >= 1]

    #remove duplicate words in same file
    new_words = list(set(split_data))
    words.extend(new_words)

#remove duplicate words in all global database
unique_words = list(set(words))
unique_words.sort()
print(unique_words)
