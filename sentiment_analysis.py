from textblob import TextBlob as tb
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
from PIL import Image
from os import path
import numpy as np
import processReviews
import string
import nltk


def create_stop_words():
    '''
    Output: stop_words: new stop words list with user added words
    '''
    nltk.download('stopwords')
    stop_words = stopwords.words('english')
    for word in ['flight', 'verified', 'review', 'airlines', 'fly', 'gate',
                 'airport', 'got', 'even', 'dallas', 'ft', 'worth', 'dfw',
                 'miami', 'mia', 'a350', 'new', 'york', 'jfk', 'via', 'los',
                 'angeles', 'chicago', 'atlanta', 'atl', 'san', 'francisco',
                 'ord', 'newark', 'aircraft', 'sydney', 'b777', 'a380', 'las',
                 'vegas', 'salt', 'lake', 'doha', 'cape', 'town', 'doh', 'lax',
                 'ife', 'air', 'lines', 'line', "i've", 'flights', 'airline',
                 'plane', 'ua', 'trip', 'flew', 'flying', 'us', 'time', 'one',
                 'told', 'hour', 'sfo', 'customer', 'seat', 'southwest',
                 'american', 'aa', 'delta', 'boeing', 'united', 'ana', 'all',
                 'nippon', 'japan', 'tokyo', 'haneda', 'denver', 'houston',
                 'narita', 'nrt', 'qatar', 'al', 'mourjan', 'airways',
                 'verified', 'jal', 'japanese', 'la', 'a330', 'singapore',
                 'bangkok', 'luggage', 'made', 'way', 'pilot', 'phoenix',
                 'another', 'around', 'take', 'day', 'go', 'much', 'take',
                 'say', 'asked', 'also', 'however', 'leg', 'much', 'though',
                 'chi', 'minh', 'would', 'get', 'could', 'back', 'really']:
        stop_words.append(word)
    return stop_words


def bag_of_words(df, positive, stop_words):
    '''
    Input: df: dataframe specifying airline reviews
    positive: 1 if you want positive reviews for airline or 0 if you wantnegative reviews
    stop_words: list of words deemed unimportant for NLP analysis
    Output: bag_of_words: string of words deemed important for NLP analysis
    '''
    class_words = []
    for x in df[df['positive'] == positive]['words']:
        for word in x.split(' '):
            if word.strip(string.punctuation).lower() not in stop_words and word:
                class_words.append(word.strip(string.punctuation).lower())
    bag_of_words = ' '.join(class_words)
    return bag_of_words


def common_trigrams(bag_of_words):
    '''
    Input: bag_of_words: string of words used for NLP analysis
    Output: Returns 5 most common trigrams in positive or negative reviews for particular airline
    '''
    tokens = bag_of_words.split(' ')
    trigrams = [(tokens[i], tokens[i+1], tokens[i+2]) for i in
                range(0, len(tokens)-2)]
    trigrams_counter = Counter(trigrams)
    index = 1
    for key, val in trigrams_counter.most_common(20):
        for key2, val2 in trigrams_counter.most_common(20)[index:]:
            if len(set(key)-set(key2)) <= 1:
                trigrams_counter[key] += trigrams_counter[key2]
                trigrams_counter.pop(key2)
        index += 1
    return trigrams_counter.most_common(5)


def create_word_cloud(bag_of_words, stop_words, title, fig):
    '''
    Input: bag_of_words: string of words used for NLP analysis
    Output: Word cloud based on words in bag_of_words in the shape of a plane! (shape of the plane-icon.png silhouette)
    '''
    d = path.dirname(__file__)
    plane_mask = np.array(Image.open(path.join(d, "plane-icon.png")))
    plt.figure(figsize=(5, 5))
    wordcloud = WordCloud(colormap='magma', background_color=None, stopwords=stop_words).generate(bag_of_words)
    plt.title(title, fontdict={'fontsize': 15})
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(fig, transparent=True)
    plt.clf()


def word_analysis(airline, dfs, stop_words, positive=1):
    '''
    Input: dfs: list of dataframes of reviews for each airline
    stop_words: words deemed unimportant for NLP analysis
    positive: 1 to get reviews with overall rating of 6 or more or 0 for reviews with overall rating of 5 or less
    Output: wordcloud of words that are most used in reviews that are either positive or negative
    '''
    airlines = airline
    i = 0
    sentiment = ''
    sentiment = 'Positive'
    for df in dfs:
        sentiment_words = bag_of_words(df, 1, stop_words)
        create_word_cloud(
            sentiment_words,
            stop_words,
            f'{airlines[i]} : {sentiment}',
            "./static/images/positive.png"
        )
        i += 1

    sentiment = 'Negative'
    i=0
    for df in dfs:
        sentiment_words = bag_of_words(df, 0, stop_words)
        create_word_cloud(
            sentiment_words,
            stop_words,
            f'{airlines[i]} : {sentiment}',
            "./static/images/negative.png"

        )
        i += 1


def trigram_analysis(airline, dfs, stop_words, positive, title):
    '''
    Input: dfs: list of dataframes of reviews for each airline
    stop_words: words deemed unimportant for NLP analysis
    positive: 1 to get reviews with overall rating of 6 or more or 0 for reviews with overall rating of 5 or less
    Output: pie graph of top 5 most used trigrams in reviews that are either positive or negative
    '''
    airlines = airline
    i = 0
    sentiment = ''
    if positive:
        sentiment = 'Positive Trigrams\n'
    else:
        sentiment = 'Negative Trigrams\n'

    for df in dfs:
        sentiment_words = bag_of_words(df, positive, stop_words)
        trigrams = common_trigrams(sentiment_words)
        labels = []
        values = []
        for k, v in trigrams:
            labels.append(' '.join(k).title())
            values.append(v)
        if positive:
            colors = ['yellowgreen', 'gold', 'lightskyblue' ,'lightcoral', 'firebrick']
        else:
            colors = ['firebrick', 'lightcoral', 'lightskyblue', 'gold', 'yellowgreen']
        explode = (0.1, 0, 0, 0, 0)
        plt.pie(values, explode=explode, labels=labels, colors=colors,
                autopct=make_autopct(values), shadow=True, startangle=90)
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.title(f'{airlines[i]} : {sentiment}', fontdict={'fontsize': 15})
        i += 1
        plt.savefig(title, transparent=True)
        plt.clf()


def make_autopct(values):
    '''
    Input: values: number of times event (trigrams) occurs in text
    Output: values to be used in pie graph
    '''
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_autopct


def sentimentAnalysis(airline, data):
    stop_words = create_stop_words()
    word_analysis([airline], data, stop_words, 0)
    trigram_analysis([airline], data, stop_words, 0, "./static/images/negative-trigram.png")
    trigram_analysis([airline], data, stop_words, 1, "./static/images/positive-trigram.png")