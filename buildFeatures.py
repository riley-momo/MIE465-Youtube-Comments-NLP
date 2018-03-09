import os
import google.oauth2.credentials
import httplib2
import sys
import nltk
import vaderSentiment
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import string
import statistics

from github import Github

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from apiclient.discovery import build


from nltk.corpus import treebank
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
from itertools import cycle
from mpl_toolkits.mplot3d import Axes3D


        


def get_comment_threads(youtube, video_id, comments):
    threads = []
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
    ).execute()
    
    #Get the first set of comments
    for item in results["items"]:
        threads.append(item)
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)
    
    #Keep getting comments from the following pages
    while ("nextPageToken" in results):
        results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        pageToken=results["nextPageToken"],
        textFormat="plainText",
        ).execute()
        for item in results["items"]:
            threads.append(item)
            comment = item["snippet"]["topLevelComment"]
            text = comment["snippet"]["textDisplay"]
            comments.append(text)
            
        #only get first 200 threads
        if len(threads) >= 200:
            break    
    #print("Total threads: %d" % len(threads))
    
    return threads
  
def get_comments(youtube, parent_id, comments):
  results = youtube.comments().list(
    part="snippet",
    parentId=parent_id,
    textFormat="plainText"
  ).execute()

  for item in results["items"]:
    text = item["snippet"]["textDisplay"]
    comments.append(text)
    #only get first 50 replies
    if len(comments) > 50 :
        break
        
  return results["items"]
  
 
    
def get_features(text):
    #init feature dictionary
    features = {}
    
    #get comment sentiment
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(text)['compound']
    features['sentiment'] = ss
    
    #tokenize
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(text)
    #convert to nltk Text
    words = nltk.Text(tokens)
    #get wordCount
    wordCount = len(words)
    features['wordCount'] = wordCount
    #get frequency distribution
    fdist = FreqDist(words)
    #store fdist in dictionary for use in creating combined fdist
    features['fDist'] = fdist
    #convert FreqDist to dictionary
    fdist = dict(fdist)
    #append FreqDist to features
    features.update(fdist)
    return features




if __name__ == '__main__':
    #Define youtube API parameters
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    DEVELOPER_KEY = 'AIzaSyD4gc2e-6lPQYg_T-kq8l9gIPtitqVhM7o'
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    #Initialize video dictionary
    videoComments = {}
    #read video Ids from csv file
    videoIds = pd.read_csv("USvideos.csv")["video_id"]
    #Iterate through video Ids
    j = 0
    for video_id in videoIds:
        print('Processing video: ' + video_id)
        try:
            #Intiliaze comment list
            comments = []
            video_comment_threads = get_comment_threads(youtube,  video_id,  comments)
            commentFeatures = {}
            #Iterate through comment threads
            for thread in video_comment_threads:
                topComment =  thread["snippet"]["topLevelComment"]
                text = topComment["snippet"]["textDisplay"]
                commentFeatures[text] = get_features(text)
                comments = get_comments(youtube, thread["id"], comments)
                #Iterate through replies
                for comment in comments:
                    text = comment["snippet"]["textDisplay"]
                    commentFeatures[text] = get_features(text)
        
        #API error handling
        except HttpError:
            print ("An HTTP error occurred")
            #skip video if we cannot retrieve comments
            continue
 
        #add comment features dictionary to video ID
        videoComments[video_id] = {}
        videoComments[video_id]['commentFeatures'] = commentFeatures
        
        #get combined frequency distribution for all comments
        i = 0
        for comment in commentFeatures:
            if i == 0:
                fdist = commentFeatures[comment]['fDist']#Initial freq dist
                del commentFeatures[comment]['fDist'] #remove after use
            else:
                fdist.update(commentFeatures[comment]['fDist']) #Update freq dist as we progress
                
                del commentFeatures[comment]['fDist'] #remove after use
            i = 1
        #convert FreqDist to dictionary
        fdist = dict(fdist)
        #append FreqDist to features
        videoComments[video_id].update(fdist)
        
        #get mean wordCount across all comments
        wordCounts = [commentFeatures[key]['wordCount'] for key in commentFeatures]
        meanWC = statistics.mean(wordCounts)
        WCStdev = statistics.stdev(wordCounts)
        videoComments[video_id]['meanWordCount'] = meanWC 
        videoComments[video_id]['wordCountStdev'] = WCStdev 
       
        #get mean sentiment across all comments
        sentiments = [commentFeatures[key]['sentiment'] for key in commentFeatures]
        meanSentiment = statistics.mean(sentiments)
        sentimentStdev = statistics.stdev(sentiments)
        videoComments[video_id]['meanSentiment'] = meanSentiment 
        videoComments[video_id]['sentimentStdev'] = sentimentStdev
        
        #----Convert data to csv----#
        
        #Convert commentFeatures to dataframe
        commentFeatureDF = pd.DataFrame.from_dict(videoComments[video_id]['commentFeatures'], orient = 'index').fillna(0)
        #Convert dataframe to csv
        commentFeatureDF.to_csv(video_id + '.csv')
        
        #remove commentFeatures now that we have exported data
        del videoComments[video_id]['commentFeatures']
        
        #only do first X videos
        if j == 50:
            break
        j+= 1
        
        
    #----Convert data to csv----#
    
    #convert videoComments to dataframe
    videoCommentsDF = pd.DataFrame.from_dict(videoComments, orient = 'index').fillna(0)
    #Convert dataframe to csv
    videoCommentsDF.to_csv('videoCommentStats.csv')