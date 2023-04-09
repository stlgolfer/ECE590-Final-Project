import numpy as np
import tensorflow as tf
from keras import layers
from keras.models import Model, load_model
# from keras.utils import plot_model
import matplotlib.pyplot as plt
from convokit import Corpus, download, download_local
import pickle
from collections import Counter
from english_words import get_english_words_set


# words = get_english_words_set(['web2'], lower=True)
# going to try and make my own statistical model
# need to load in any extra words in saved_words, if available
to_append = pickle.load(open('./saved_words.pkl', 'rb'))
words = ['yuh', 'dank', 'yuhboi'] + to_append # given at least first two characters

# keys will be the number of characters available, the tree will have the words with associated probabilities
nstubtree = {}

MAX_STEM_LENGTH = 3
for sl in range(2,MAX_STEM_LENGTH+1):
    words_cleaned = [len(x) <= sl + 1 for x in words]
    tree = {} # will have a key with first two characters, then it will iterate through the rest of the words and append any endings it finds

    # reject all words that have length less than or equal to 3
    for wi in words:
        key = wi[0:sl]
        if key not in tree:
            tree[key] = [wi[sl:]] # add its ending
        else:
            # append it's ending
            tree[key].append(wi[sl:])
    nstubtree[sl] = tree

print(nstubtree)
with open('./autocomplete.pkl', 'wb') as f:
    pickle.dump(nstubtree, f)

def predictn(stem: str, tree: dict, threshold: float) -> str:
    if stem not in tree:
        return ''
    # for now just print the options
    counted = Counter(tree[stem])
    print(counted)
    # we now have the counts, so just normalize against the total
    for k in counted.keys():
        counted[k] = counted[k]/len(counted.values())
    print(counted)
    # now only return an autocompleted word that meets the criteria. select the first one that 'comes to mind'
    for candidate in counted.keys():
        if counted[candidate] >= threshold:
            return stem + candidate
    return '' # didn't find one :(

def predict(stem: str, tree: dict, thresh: float) -> str:
    if len(stem) not in tree:
        return ''
    else:
        # there's a key for it
        return predictn(stem, tree[len(stem)], thresh)

# print(predict('yuhb', nstubtree, 0.5))
