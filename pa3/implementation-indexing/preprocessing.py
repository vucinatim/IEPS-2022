from operator import index
from nltk.tokenize import word_tokenize
from stopwords import stop_words_slovene
import numpy as np


def preprocess_text(txt):
    txt = txt.lower()
    words = txt.split()
    tokens, indexes = [], []
    for idx, w in enumerate(words):
        word_tokens = word_tokenize(w)
        tokens_wo_stopwords = [t for t in word_tokens if t not in stop_words_slovene]
        tokens.extend(tokens_wo_stopwords)
        indexes.extend([idx for _ in range(len(tokens_wo_stopwords))])

    return np.array(tokens), np.array(indexes)
