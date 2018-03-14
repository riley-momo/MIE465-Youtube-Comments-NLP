import os
import google.oauth2.credentials
import httplib2
import sys
import nltk
import vaderSentiment
import numpy as np
import pandas as pd
import string
import statistics

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from apiclient.discovery import build


from nltk.corpus import treebank
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



        


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
    #only get first 30 replies
    if len(comments) > 30 :
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
    #Iterate through unique video Ids
    j = 0
    for video_id in set(videoIds):
        #print progress message
        print('Processing video # ' + str(j) +'/4000, ' + video_id)
        
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
        commentFeatureDF.to_csv('video_csvs/' + video_id + '.csv')
        
        #remove commentFeatures now that we have exported data
        del videoComments[video_id]['commentFeatures']
        
        #do first 4000 videos
        if j == 4000:
            break
        j+= 1
        
        
    #----Convert data to csv----#
    
    #convert videoComments to dataframe
    videoCommentsDF = pd.DataFrame.from_dict(videoComments, orient = 'index').fillna(0)
    #Convert dataframe to csv
    videoCommentsDF.to_csv('videoCommentStats.csv')