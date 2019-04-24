from nltk import word_tokenize, sent_tokenize, pos_tag
from nltk.stem import PorterStemmer
import string
from nltk.corpus import stopwords
from collections import Counter
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

test_script = '/Users/ivywang/PycharmProjects/movie_ratings/script_file_upload.txt'


def preprocess(text, lower=False):
    tokens = word_tokenize(text)
    if lower:
        tokens = [token.lower() for token in tokens]
    ps = PorterStemmer()
    tokens_stemmed = [ps.stem(token) for token in tokens]
    # tokens_nopunc = [tok for tok in tokens_stemmed if tok not in string.punctuation]
    tokens_nostop = [tok for tok in tokens_stemmed if tok not in set(stopwords.words('english'))]

    return " ".join(tokens_nostop)

with open(test_script, 'r') as file:
    script = file.read()

# print(script)
# print(preprocess(script))
word_list = preprocess(script)
print(word_list)


# this function makes a dictionary of all words in script, value is the word count
def word_count_all(list):
    # list is a
    all_word_count = {}
    all_words_list = []
    for script in list:
        word_list = preprocess(script).split()
        all_words_list.append(word_list)
    all_words_list = [item for sublist in all_words_list for item in sublist]
    for word in all_words_list:
        all_word_count[word] = all_word_count.get(word, 0) +1
    return all_word_count
#
# # create matrix, return TF of all words
# def computeTF(wordDict, all_words_list):
#     tfDict = { }
#     bowCount = len(all_words_list)
#     for word, count in wordDict.items():
#         tfDict[word] = count/float(bowCount)
#     return tfDict
#
# # create IDF , return IDF dictionary of all words
# def computeIDF(docList):
#     import math
#     idfDict = {}
#     N = len(docList)
#     idfDict = dict.fromkeys(docList[0].keys(), 0)
#     for doc in docList:
#         for word, val in doc.items():
#             if val > 0:
#                 idfDict[word] += 1
#     for word, val in idfDict.items():
#         idfDict[word] = math.log10(N/float(val))
#
#     return idfDict
#
# # idfs is the idfDict, tfBow is tfDict, computes the final TFIDF score
# def computeTFIDF(wordDict, all_words_list, tfBow, idfs):
#     tfBow = computeTF(wordDict, all_words_list)
#
#     tfidf = {}
#     for word, val in tfBow.items():
#         tfidf[word] = val * idfs[word]
#     return tfidf

# calculate the mean number of word per utterane; takes the sum of all words in all utterance over number of utterance
def mean_words_per_sentence(script):
    utterances = sent_tokenize(script)
    number_utterances = len(utterances)
    sum_num_words = 0
    for sent in utterances:
        sent_tokens = word_tokenize(sent)
        sum_num_words += len(sent_tokens)
    mean = sum_num_words / number_utterances
    return utterances, mean



# make vector
vectorizer = TfidfVectorizer("content", lowercase=True, analyzer="word", use_idf=True, min_df=10)
with open('/Users/ivywang/PycharmProjects/movie_ratings/script_file.txt', 'r') as scripts_file:
    script_list = []
    rating_list = []
    file = scripts_file.read()
    for line in file[:10]:
        fields = line.split('\t')
        # print(fields[0])
        script_list.append(fields[2]) # script list is the script
        rating_list.append(float(fields[1]))

# create a list of mean nu
mean_list = []
for one_script in script_list:
    mean = mean_words_per_sentence(one_script)
    mean_list.append(mean)

mean_array = np.asarray(mean_list)
print(mean_array)
X = vectorizer.fit_transform(script_list)
X_array = np.toarray(X)
print(X_array)
for i, list in X_array:
    list.append(mean_list[i])
print(X_array)
# y = rating_list
y = np.asarray(rating_list)



# split data

# train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.3)

# print(train_X)
# # print(train_y)
#
# # training
# # generate regression dataset
# # fit final model
# model = LinearRegression()
# fitted = model.fit(train_X, train_y)
# predicted = model.predict(val_X)

# print(predicted)
# # print(val_y)
#
# # Round to integer
# pre = [round(x) for x in predicted]
# test_y = [round(x) for x in val_y]
#
# # correlation index
# print(np.corrcoef(pre, test_y))
# print(np.corrcoef(predicted, val_y))
#
# scored = model.score(val_X, val_y)
# # print(scored)
