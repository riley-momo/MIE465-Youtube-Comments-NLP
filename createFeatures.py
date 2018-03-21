import os
import httplib2
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import string
import statistics
import nltk
import Algorithmia

from collections import Counter

from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import *

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def getFeatures(comments):
    features = {}
    
    #initialize profanity filter
    client = Algorithmia.client('simlyRpEh3jOufiSoZtvLACnR8p1')
    algo = client.algo('nlp/ProfanityDetection/1.0.0')
    
    #Create frequency distribution for wordcounts of comments
    tokenizer = RegexpTokenizer(r'\w+')
    lengths = (len(tokenizer.tokenize(comment)) for comment in comments)
    wordCountDist = Counter(lengths)
    #give keys better names
    for key in wordCountDist:
        wordCountDist['wordCount' + str(key)] = wordCountDist.pop(key) 
    
    features.update(wordCountDist)
    #create combined text
    combinedText = ' '.join(comments)
    #find profanity frequency
    profanity = algo.pipe(combinedText).__dict__['result']
    profanitySum = sum(d for d in profanity.values())
    features['profanitySum'] = profanitySum
    
    #Normalize Text
    
    
    #tokenize
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(combinedText)
    #convert to nltk Text
    words = nltk.Text(tokens)
    
    #Lemmatize text 
    stemmer = PorterStemmer()
    stemmedText = [stemmer.stem(w) for w in words]
    
    
    #get frequency distribution
    fdist = FreqDist(words)
    #convert FreqDist to dictionary
    fdist = dict(fdist)
    #append FreqDist to features
    features.update(fdist)
    
    
    
   
    
    
    
    
    
    return features


    
    
    
    
    

if __name__ == '__main__':

    
    path = os.getcwd() + '\\video_csvs'
    #init video Dictionary
    videoData = {}
    #iterate through each video file
    for filename in os.listdir(path):
        #obtain video_id
        video_id = filename[:-4]
        print('Processing video: ' + video_id)
        #obtain comment data
        data = pd.read_csv(path + '\\' + filename, lineterminator='\n')
        #iterate through comments
        comments = []
        for index, d in data.iterrows():
            #append comment
            comments.append(d[0])
        #obtain features and store in data dictionary
        videoData[video_id] = getFeatures(comments)
    #export to csv