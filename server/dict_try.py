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

my_dict = {"test": 1, "testing": 2}

f = open("file.pkl","wb")
pickle.dump(my_dict,f)
f.close()

dict_ad = pickle.load( open( "file.pkl", "rb" ) )

print(dict_ad['test'], dict_ad['testing'])
