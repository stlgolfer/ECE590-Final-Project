# we'll need a few things: the dataset and the model, and the necessary imports
import pickle

import keras.models
import pandas as pd
import os
import numpy as np

import tensorflow as tf
from keras_preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Bidirectional
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import nltk; nltk.download('punkt')
import convokit
from convokit import Corpus, download, download_local

# corpus = Corpus(download_local('movie-corpus', 'C:/Users/stlgo/.convokit/downloads'))
# MAX_DIMENSIONS = 100
# df = corpus.get_utterances_dataframe().iloc[0:MAX_DIMENSIONS, :] # gotta make this smaller somehow ig
# key = 'text'
#
# # need to get tokenizer
# df[key]
# df[key] = df[key].apply(lambda x: x.replace(u'\xa0',u' '))
# df[key] = df[key].apply(lambda x: x.replace('\u200a',' '))
# tokenizer = Tokenizer(oov_token='<oov>') # For those words which are not found in word_index
# tokenizer.fit_on_texts(df[key])
#
# # region: from generator
# input_sequences = []
# for line in df[key]:
#     token_list = tokenizer.texts_to_sequences([line])[0]
#     # print(token_list)
#
#     for i in range(1, len(token_list)):
#         n_gram_sequence = token_list[:i + 1]
#         input_sequences.append(n_gram_sequence)
#
# # print(input_sequences)
# print("Total input sequences: ", len(input_sequences))
# #endregion
#
# # pad sequences
# max_sequence_len = max([len(x) for x in input_sequences])

# load meta from pickle file
with open('tokenizer.pkl', 'rb') as fp:
    meta = dict(pickle.load(fp))
    tokenizer = meta['tokenizer']
    max_sequence_len = meta['max_sequence_len']

def find_next_word(seed_text, next_words):
    # actually load the model
    model = keras.models.load_model('../model_trained')

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        # predicted = model.predict_classes(token_list, verbose=0)
        #TODO: adjust threshold
        # predicted = (model.predict(token_list) > 0.005).astype("int32")
        predicted = np.argmax(model.predict(token_list), axis=-1)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    print(seed_text)