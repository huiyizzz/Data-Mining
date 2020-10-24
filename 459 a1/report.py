# The code is provided by TA
import numpy
import pandas as pd
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from PIL import Image


def remove_url_punctuation(X):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    replace_url = url_pattern.sub(r'', str(X))
    punct_pattern = re.compile(r'[^\w\s]')
    no_punct = punct_pattern.sub(r'', replace_url).lower()
    return no_punct


def split_words(X):
    split_words_list = X.split(' ')
    return split_words_list


def remove_words(X):
    global stop_words
    words = []
    for word in X:
        if (word not in stop_words and len(word) > 2 and
                word != 'nan' and word not in words):
            words.append(word)
    return words


columns = ['id', 'text']
df = pd.read_csv('D1.txt', names=columns, sep='\t', lineterminator='\n',
                 error_bad_lines=False, encoding='latin1')
df2 = pd.read_csv('D2.txt', names=columns, sep="\t", lineterminator='\n',
                  error_bad_lines=False, encoding='latin1')
# remove punctuation
df['tidy_tweet'] = df['text'].apply(remove_url_punctuation)
df2['tidy_tweet'] = df2['text'].apply(remove_url_punctuation)
# tokenize words
df['word_list'] = df['tidy_tweet'].apply(split_words)
df2['word_list'] = df2['tidy_tweet'].apply(split_words)

# remove stop words and the same words
global stop_words
stop_words = set(stopwords.words('english'))
df['nlp_tweet'] = df['word_list'].apply(remove_words)
df2['nlp_tweet'] = df2['word_list'].apply(remove_words)

# word frequency
all_words_unique_list = (df['nlp_tweet'].explode()).unique()
print('The numbers of unique tokens of D1:', len(all_words_unique_list))
word_list = list(df['nlp_tweet'].explode())
nltk_count = nltk.FreqDist(word_list)
normalized_count = {}
for k, v in nltk_count.most_common(100):
    normalized_count[k] = v/1000
print('Top 100 most frequent tokens in D1:')
print(normalized_count)

all_words_unique_list2 = (df2['nlp_tweet'].explode()).unique()
print('The numbers of unique tokens of D2:', len(all_words_unique_list2))
word_list2 = list(df2['nlp_tweet'].explode())
nltk_count2 = nltk.FreqDist(word_list2)
normalized_count2 = {}
for k, v in nltk_count2.most_common(100):
    normalized_count2[k] = v/1000
print('Top 100 most frequent tokens in D2:')
print(normalized_count2)

# make word cloud
wordCloud1 = WordCloud(background_color='white', colormap='Purples'
                       ).generate_from_frequencies(nltk_count)
wordCloud1.to_file("D1.png")

wordCloud2 = WordCloud(background_color='white', colormap='summer'
                       ).generate_from_frequencies(nltk_count2)
wordCloud2.to_file("D2.png")
