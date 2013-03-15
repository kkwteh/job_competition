#!/Users/teh/code/kaggle/ENV/bin/python
"""
This script loads the 1% minified version of the training data into
a pandas dataframe and constructs features corresponding to words
appearing in the job titles and then stores the enhanced dataframe
into a csv file.
"""

import numpy as np
import string
import operator
import pandas as pd
from collections import Counter
from nltk.tokenize import wordpunct_tokenize
import re


def appearances(word, string):
    """Counts the number of times the word appears, whole, in the string
    """
    return len(re.findall(r'\b' + word + r'\b', string))


def add_word_count_feature(df, word, attr_name):
    """Adds a feature to a dataframe corresponding to the number of times the
    given word appears in the column specified by attr_name.

    Args:
    df: the dataframe which will have a feature added to it
    word: the word to be counted for the new feature
    attr_name: the column which contains the text where the word will be counted
    Returns:
    Nothing -- the dataframe is modified in place
    """
    attr = operator.attrgetter(attr_name)
    evaluated_feature_as_list = [appearances(word, text.lower()) for text
                                                                in attr(df)]
    df[attr_name + "_has_" + word] = pd.Series(evaluated_feature_as_list,
                                                    index=df.index)
def has_punct(word):
    """Returns True if word contains punctuation and False otherwise
    """
    for char in word:
        if char in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
            return True
    return False


def is_printable(word):
    """Returns True if word has only printable characters and False otherwise
    """
    for char in word:
        if char not in string.printable:
            return False
    return True


train = pd.read_csv("mini_Train_rev1.csv")
valid = pd.read_csv("Valid_rev1.csv")

def count_words_in_column(df, attr_name):
    """Counts all of the words appearing in a column of a data frame
    Args:
    df: The data frame whose column will be counted
    attr_name: A string containing the attribute name of the column
    Returns:
    A collections.Counter() object containing counts of all words appearing
    in the column
    """

    attr = operator.attrgetter(attr_name)
    attr_words = Counter()
    for text in attr(df):
        for word in wordpunct_tokenize(text):
            if (has_punct(word) == False) and (is_printable(word) == True):
                attr_words[word.lower()] += 1
    return attr_words


title_words = count_words_in_column(train, "Title")
for word, count in title_words.items():
    add_word_count_feature(train, word, "Title")
    add_word_count_feature(valid, word, "Title")

with open('enhanced_mini_train.csv','wb') as f:
    train.to_csv(f)

with open('enhanced_valid.csv','wb') as f:
    valid.to_csv(f)
