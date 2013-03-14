#!/Users/teh/code/kaggle/ENV/bin/python
"""
This script loads the 1% minified version of the training data into
a pandas dataframe and constructs features corresponding to words
appearing in the job titles and then stores the enhanced dataframe
into a csv file.
"""

import numpy as np
import string
import pandas as pd
from collections import Counter
from nltk.tokenize import wordpunct_tokenize
import re


def appearances(word, string):
    return len(re.findall(r'\b' + word + r'\b', string))


def add_title_feature(train, word):
    evaluated_feature_as_list = [appearances(word, title.lower()) for title
                                                                in train.Title]
    train["title_has_" + word] = pd.Series(evaluated_feature_as_list,

                                                    index=train.index)
def has_punct(word):
    for char in word:
        if char in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
            return True
    return False


def is_printable(word):
    for char in word:
        if char not in string.printable:
            return False
    return True


train = pd.read_csv("mini_Train_rev1.csv")

title_words = Counter()
for text in train.Title:
    for word in wordpunct_tokenize(text):
        if (has_punct(word) == False) and (is_printable(word) == True):
            title_words[word.lower()] += 1

title_word_items = title_words.items()
title_word_items.sort(key= lambda (k,v): -v)

for word, count in title_word_items:
    add_title_feature(train, word)

with open('enhanced_mini_train.csv','wb') as f:
    train.to_csv(f)
