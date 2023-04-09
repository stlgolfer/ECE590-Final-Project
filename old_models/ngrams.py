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
from convokit import Corpus, download
import pickle

# code mostly from https://www.kaggle.com/code/ysthehurricane/next-word-prediction-bi-lstm-tutorial-easy-way/input
# good data set possibly from cornell: https://github.com/niderhoff/nlp-datasets
# http://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html
# https://github.com/CornellNLP/ConvoKit/tree/0e44dd838df191a22c6ba0548a44f8e3d26d34cb
# medium_data = pd.read_csv('./medium_data.csv')
# medium_data.head()

model = None
print(len(os.listdir('../model_trained')))
# make and train the model
# will need to do a bit of preprocessing to connect cornell db to regular db
corpus = Corpus(download('movie-corpus'))
df = corpus.get_utterances_dataframe().iloc[0:7000, :] # gotta make this smaller somehow ig
key = 'text'


print("Number of records: ", df.shape[0])
print("Number of fields: ", df.shape[1])

df[key]
df[key] = df[key].apply(lambda x: x.replace(u'\xa0',u' '))
df[key] = df[key].apply(lambda x: x.replace('\u200a',' '))
tokenizer = Tokenizer(oov_token='<oov>') # For those words which are not found in word_index
tokenizer.fit_on_texts(df[key])
total_words = len(tokenizer.word_index) + 1

print("Total number of words: ", total_words)
print("Word: ID")
print("------------")
# print("<oov>: ", tokenizer.word_index['<oov>'])
# print("Strong: ", tokenizer.word_index['strong'])
# print("And: ", tokenizer.word_index['and'])

input_sequences = []
for line in df[key]:
    token_list = tokenizer.texts_to_sequences([line])[0]
    # print(token_list)

    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i + 1]
        input_sequences.append(n_gram_sequence)

# print(input_sequences)
print("Total input sequences: ", len(input_sequences))

# pad sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
input_sequences[1]

# need to cache input_sequences and the tokenizer to speed up load times
with open('tokenizer.pkl', 'wb') as f:
    pickle.dump({'tokenizer': tokenizer, 'max_sequence_len': max_sequence_len}, f)

xs, labels = input_sequences[:,:-1],input_sequences[:,-1]
ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

print(xs[5])
print(labels[5])
print(ys[5][14])
model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
model.add(Bidirectional(LSTM(150)))
model.add(Dense(total_words, activation='softmax'))
adam = Adam(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
history = model.fit(xs, ys, epochs=50, verbose=1)
#print model.summary()
print(model)
model.save('./model_trained')

def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.show()