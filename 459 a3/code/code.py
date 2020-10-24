import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from scipy.optimize import curve_fit
import math


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
    words = []
    for word in X:
        if word != 'nan' and word != '' and word not in words:
            words.append(word)
            
    return words


def get_result(sets, max_length):
    if max_length == 5:
        result = [[], [], [], [], []]
    if max_length == 4:
        result = [[], [], [], []]
    for length in range(1, max_length+1):
        subset = sets[(sets['length'] == length)]
        print(len(subset.index))
        if max_length == 5:
            subset = subset.head(100)
        pattern_list = subset.values.tolist()
        for pattern in pattern_list:
            temp = []
            itemset = list(pattern[1])
            temp.append(itemset)
            temp.append(pattern[0])
            result[length-1].append(temp)

    return result


def patterns(dataset, support, max_length):
    te = TransactionEncoder()
    df_tf = te.fit_transform(dataset)
    df = pd.DataFrame(df_tf, columns=te.columns_)
    sets = apriori(df, min_support=support, use_colnames=True,
                   max_len=max_length)
    sets['length'] = sets['itemsets'].apply(lambda x: len(x))
    sets['support'] = sets['support'] * 1000
    sets['support'] = sets['support'].astype(int)
    sets.sort_values(['length', 'support'], ascending=False, inplace=True)
    return sets


def find_odd(D1, D2):
    odd_dict = {}
    odd_result = []
    list_D1 = get_result(D1, 4)
    list_D2 = get_result(D2, 4)

    for length in range(0, 4):
        for itemset in list_D1[length]:
            for item in list_D2[length]:
                if all(elem in itemset[0] for elem in item[0]):
                    temp = frozenset(itemset[0])
                    odd_value = item[1] / itemset[1]
                    odd_dict[temp] = odd_value
    odd = sorted(odd_dict.items(), key=lambda x: x[1], reverse=True)
    odd = odd[0:100]
    for pair in odd:
        temp = []
        term = list(pair[0])
        temp.append(term)
        temp.append(pair[1])
        odd_result.append(temp)

    return odd_result


def func(x, a, c):
    return a*pow(x, -c)


columns = ['id', 'text']
df1 = pd.read_csv('D1.txt', names=columns, sep='\t', lineterminator='\n',
                  error_bad_lines=False, encoding='latin1')
df2 = pd.read_csv('D2.txt', names=columns, sep="\t", lineterminator='\n',
                  error_bad_lines=False, encoding='latin1')

df1['tidy_tweet'] = df1['text'].apply(remove_url_punctuation)
df2['tidy_tweet'] = df2['text'].apply(remove_url_punctuation)
df1['word_list'] = df1['tidy_tweet'].apply(split_words)
df2['word_list'] = df2['tidy_tweet'].apply(split_words)

df1['nlp_tweet'] = df1['word_list'].apply(remove_words)
df2['nlp_tweet'] = df2['word_list'].apply(remove_words)


# question 3
set1 = patterns(df1['nlp_tweet'], 0.01, 5)
set2 = patterns(df2['nlp_tweet'], 0.025, 5)
D1_result = get_result(set1, 5)
D2_result = get_result(set2, 5)

for length in range(0, 5):
    print('The top 100 length-'+str(length+1), 'patterns for D1:')
    print(D1_result[length])
for length in range(0, 5):
    print('The top 100 length-'+str(length+1), 'patterns for D2:')
    print(D2_result[length])


# question 3.3
most_frequent_1 = [D1_result[index][0][1] for index in range(0, 5)]
most_frequent_2 = [D2_result[index][0][1] for index in range(0, 5)]
X = [1, 2, 3, 4, 5]

popt1, pcov1 = curve_fit(func, X, most_frequent_1)
print('The parameters are a='+str(popt1[0]), 'and c='+str(popt1[1]))
popt2, pcov2 = curve_fit(func, X, most_frequent_2)
print('The parameters are a='+str(popt2[0]), 'and c='+str(popt2[1]))

Xnew = np.arange(1, 5, 0.1)
Y1 = func(Xnew, popt1[0], popt1[1])
Y2 = func(Xnew, popt2[0], popt2[1])

plt.figure(1)
plt.plot(X, most_frequent_1, '.-', color='firebrick', label='D1')
plt.plot(X, most_frequent_2, '.-', color='olive', label='D2')
plt.xlabel('Length k')
plt.ylabel('Support')
plt.legend()
plt.title('The Plot of the Support of the Most Frequent Pattern at Length k')

plt.figure(2)
plt.plot(X, most_frequent_1, '*', color='firebrick', label='Actual D1')
plt.plot(Xnew, Y1, label='Power Law Distribution')
plt.xlabel('Length k')
plt.ylabel('Support')
plt.legend()
plt.title('The Distribution of D1')

plt.figure(3)
plt.plot(X, most_frequent_2, '*', color='olive', label='Actual D2')
plt.plot(Xnew, Y2, label='Power Law Distribution')
plt.xlabel('Length k')
plt.ylabel('Support')
plt.legend()
plt.title('The Distribution of D2')
plt.show()


# question 4
set1_4 = patterns(df1['nlp_tweet'], 0.005, 4)
set2_4 = patterns(df2['nlp_tweet'], 0.020, 4)
odd_result = find_odd(set1_4, set2_4)
print(odd_result)
