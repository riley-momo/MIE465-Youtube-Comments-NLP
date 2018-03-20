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

from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
from nltk.probability import FreqDist

def getFeatures(comments):
    features = {}
    
    #initialize profanity filter
    client = Algorithmia.client('simlyRpEh3jOufiSoZtvLACnR8p1')
    algo = client.algo('nlp/ProfanityDetection/1.0.0')
    
    #create combined text
    combinedText = ' '.join(comments)
    #find profanity frequency
    profanity = algo.pipe(combinedText).__dict__['result']
    profanitySum = sum(d for d in profanity.values())
    #tokenize
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(combinedText)
    #convert to nltk Text
    words = nltk.Text(tokens)
    #get wordCount
    # wordCount = len(words)
    # features['wordCount'] = wordCount
    #get frequency distribution
    fdist = FreqDist(words)
    #find words to clean
    wordsToRemove = sorted(w for w in set(words) if len(w) < 5 and fdist[w] < 2)
    #convert FreqDist to dictionary
    fdist = dict(fdist)
    #append FreqDist to features
    features.update(fdist)
    
    
    ## WIP ##
    
   
    
    
    
    
    
    return features


    
    
    
    
    

if __name__ == '__main__':

    
    path = '\\\\SRVA\Homes$\\moherril\\Documents\\Analytics in Action\\Project\\video_csvs'
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
        #obtain features
        features = getFeatures(comments)
    #export to csv