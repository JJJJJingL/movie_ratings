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
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import pearsonr
import pandas as pd
import argparse


def preprocess(text, lower=False):
    """ preprocessed the text, lowering as optional, otherwise stem, and takes away stopwords"""
    tokens = word_tokenize(text)
    if lower:
        tokens = [token.lower() for token in tokens]
    ps = PorterStemmer()
    tokens_stemmed = [ps.stem(token) for token in tokens]
    # tokens_nopunc = [tok for tok in tokens_stemmed if tok not in string.punctuation]
    tokens_nostop = [tok for tok in tokens_stemmed if tok not in set(stopwords.words('english'))]

    return " ".join(tokens_nostop)


# this function
def word_count_all(list):
    """makes a dictionary of all words in script, value is the word count"""
    all_word_count = {}
    all_words_list = []
    for script in list:
        word_list = preprocess(script).split()
        all_words_list.append(word_list)
    all_words_list = [item for sublist in all_words_list for item in sublist]
    for word in all_words_list:
        all_word_count[word] = all_word_count.get(word, 0) + 1
    return all_word_count


def mean_words_per_sentence(script):
    """calculate the mean number of word per utterane; takes the sum of
     all words in all utterance over number of utterance"""
    utterances = sent_tokenize(script)
    # the number of sentences in this script
    number_utterances = len(utterances)
    sum_num_words = 0
    #  num_words =[]
    for sent in utterances:
        sent_tokens = word_tokenize(sent)
        #     num_words.append(len(sent_tokens))
        sum_num_words += len(sent_tokens)
    mean = sum_num_words / number_utterances

    return utterances, mean, number_utterances


def add_pos_tag(script):
    """returns the respective percentage of nouns, adjectives, and verbs
    (among all nouns, adjectives, and verbs) in the one script"""

    text = word_tokenize(script)
    total_words = len(text)
    script_tagged = pos_tag(text)
    num_noun = 0
    num_adj = 0
    num_verb = 0
    for token, tag in script_tagged:
        if tag.startswith('N'):
            num_noun += 1
        if tag.startswith('J'):
            num_adj += 1
        if tag.startswith('V'):
            num_verb += 1

    percentage_n = num_noun / total_words
    percentage_adj = num_adj / total_words
    percentage_v = num_verb / total_words
    return percentage_n, percentage_adj, percentage_v


# split datasets
def data_split(X, y):
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state = 42)
    train_X, val_X, train_y, val_y = train_test_split(train_X, train_y, test_size=0.2, random_state = 42)
    return train_X, train_y, test_X, test_y, val_X, val_y

def random_forest(train_X, train_y, val_X, val_y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(train_X, train_y)
    predicted = model.predict(val_X).reshape(-1,1)
    # print(predicted)
    error = abs(predicted - val_y)
    # print(round(np.mean(error), 2))
    # Calculate mean absolute percentage error (MAPE)
    mape = 100 * (error / val_y)
    # Calculate and display accuracy
    accuracy = 100 - np.mean(mape)
    # print(f'mean words + number of sentences accuracy: {accuracy}')
    forest_corr, p_value = pearsonr(predicted, val_y)
    # print(forest_corr)
    return accuracy, forest_corr

# linear regression
def linear_model(train_X, train_y, val_X, val_y):
    model_linear_mean = LinearRegression()
    model_linear_mean.fit(train_X, train_y)
    predicted_linear = model_linear_mean.predict(val_X)
    score_linear = model_linear_mean.score(val_X, val_y)
    # print(score_linear)
    correlation_linear, p_value = pearsonr(predicted_linear, val_y)
    # print(correlation_linear)
    return score_linear, correlation_linear


def main(script_file):
    mean_list = []
    baseline_list = []
    percentage_n_list = []
    percentage_a_list = []
    percentage_v_list = []
    script_list = []
    rating_list = []

    # read cleaned data file into lists, length 890 in total
    with open(script_file, 'r') as scripts_file:
        file = scripts_file.readlines()
        for line in file:
            fields = line.split('\t')
            rating_list.append(float(fields[1]))
            script = fields[2]
            script_list.append(script)  # script list is the script
            temp_n, temp_a, temp_v = add_pos_tag(script)
            percentage_n_list.append(temp_n)
            percentage_a_list.append(temp_a)
            percentage_v_list.append(temp_v)
            utterances, mean, number_sent = mean_words_per_sentence(script)
            baseline_list.append(number_sent)
            if mean < 50:
                mean_list.append(mean)
            else:
                mean_list.append(0)

    # Due to the punctuation variation of original scripts, we need to exclude the mean > 100,
    # and correspondingly, get rid of these items in all of the other feature list
    # 890-> 824
    script_list_stripped = [script for i, script in enumerate(script_list) if mean_list[i] is not 0]  # 824
    mean_list_stripped = [mean for mean in mean_list if mean is not 0]
    rating_list_stripped = [rating for i, rating in enumerate(rating_list) if mean_list[i] is not 0]
    baseline_list_stripped = [b for i, b in enumerate(baseline_list) if mean_list[i] is not 0]
    percentage_a_list_str = [b for i, b in enumerate(percentage_a_list) if mean_list[i] is not 0]
    percentage_n_list_str = [b for i, b in enumerate(percentage_n_list) if mean_list[i] is not 0]
    percentage_v_list_str = [b for i, b in enumerate(percentage_v_list) if mean_list[i] is not 0]

    # make the above lists into numpy arrays and reshape
    # baseline array:
    X_base = np.asarray(baseline_list_stripped).reshape(-1, 1)
    # print(f'the array shape of baseline feature is: {X_base.shape}')

    # mean words per sentence numpy array
    mean_array = np.asarray(mean_list_stripped)
    X_mean = mean_array.reshape(-1, 1)
    X_mean = X_mean.reshape(-1, 1)
    # print(f'the array shape of mean-words-per-sentence feature is: {X_mean.shape}')

    # TFIDF vector --> numpy array
    vectorizer = TfidfVectorizer("content", lowercase=True, analyzer="word", use_idf=True, min_df=10)
    vectorizer.fit(script_list_stripped)
    tfidf_list = []
    for script in script_list_stripped:
        script_vector = vectorizer.transform([script])
        tfidf = script_vector.toarray()
        tfidf_list.append(tfidf)
        # print(tfidf)
    X_tfidf = np.vstack(tfidf_list)
    # print(f'the array shape of TFIDF feature is: {X_tfidf.shape}')

    # make TFIDF and mean-words-per-sentence combined matrix:
    X_tfidf_mean = np.column_stack((X_mean, X_tfidf))

    # make labels numpy array
    y = np.asarray(rating_list_stripped)
    y = y.reshape(-1, 1)
    # print(f'the array shape of label is:{y.shape}')

    # make part of speech percentage arrays, individual and combined
    X_pos_a = np.asarray(percentage_a_list_str)
    X_pos_n = np.asarray(percentage_n_list_str)
    X_pos_v = np.asarray(percentage_v_list_str)
    X_pos = np.column_stack((X_pos_a, X_pos_n, X_pos_v))
    # print(f'the array shape of POS tag features is:{X_pos.shape}')

    # make the combined matrix containing mean-words-per-sentence, percentage of lexical items, and TFIDF:
    X_all = np.column_stack((X_mean, X_tfidf, X_pos_v, X_pos_a, X_pos_n))
    # print(f'the array shape of combined TFIDF, mean-words-per-sent, and POS tags feature is:{X_all.shape}')

    # create lists for Dataframe
    linear_score_list = []
    forest_score_list = []
    linear_corr_list = []
    forest_corr_list = []

    # evaluate two models on validation data
    feature_matrices = [X_base, X_tfidf, X_tfidf_mean, X_mean, X_pos, X_all]
    for feature in feature_matrices:
        train_X, train_y, test_X, test_y, val_X, val_y = data_split(feature, y)
        linear_model_score, pearson_corr = linear_model(train_X, train_y, val_X, val_y)
        linear_score_list.append(linear_model_score)
        linear_corr_list.append(pearson_corr)

        forest_accuracy, forest_corr = random_forest(train_X, train_y, val_X, val_y)
        forest_score_list.append(forest_accuracy)
        forest_corr_list.append(forest_corr)

    df_dict = {'feature matrices': ['baseline', 'TFIDF', 'TFIDF + mean-words-per-sentence',
                                    'mean-words-per-sentence', 'POS percentages',
                                    'TFIDF + mean-words-per-sentence + POS tag'],
               'linear model score': linear_score_list,
               'linear model correlation': linear_corr_list,
               'forest accuracy': forest_score_list,
               'forest correlation': forest_corr_list}
    df = pd.DataFrame.from_dict(df_dict)
    df['forest accuracy']= round(df['forest accuracy'] / 100, 3)

    print(df)

    # final eval on test dataset
    linear_score_test = []
    forest_score_test = []
    linear_corr_test = []
    forest_corr_test = []
    feature_matrices_test = [X_base, X_tfidf_mean]
    for f in feature_matrices_test:
        train_X, train_y, test_X, test_y, val_X, val_y = data_split(f, y)
        linear_model_score, pearson_corr = linear_model(train_X, train_y, test_X, test_y)
        linear_score_test.append(linear_model_score)
        linear_corr_test.append(pearson_corr)

        forest_accuracy, forest_corr = random_forest(train_X, train_y, test_X, test_y)
        forest_score_test.append(forest_accuracy)
        forest_corr_test.append(forest_corr)

    df_dict_test = {'feature matrices': ['baseline', 'TFIDF + mean-words-per-sentence'],
                    'linear model score': linear_score_test,
                    'linear model correlation': linear_corr_test,
                    'forest accuracy': forest_score_test,
                    'forest correlation': forest_corr_test}
    df_test = pd.DataFrame.from_dict(df_dict_test)
    df_test['forest accuracy']= round(df_test['forest accuracy'] / 100, 3)

    print(df_test)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process cleaned data file')

    parser.add_argument('-f', '--file', default='script_file.txt', help='cleaned datafile')

    args = parser.parse_args()
    main(args.file)

