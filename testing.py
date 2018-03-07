#Initial tests

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


from github import Github

from apiclient.discovery import build_from_document
from apiclient.errors import HttpError
from apiclient.discovery import build


from nltk.corpus import treebank
from nltk import word_tokenize


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs
from itertools import cycle
from mpl_toolkits.mplot3d import Axes3D

def githubTest():
    #test github API connectivity
    g = Github("user", "password")

    for repo in g.get_user().get_repos():
        print(repo.name)
        repo.edit(has_wiki=False)
        

   

  
  

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
            
        if len(threads) >= 150:
            break    
    print("Total threads: %d" % len(threads))
    
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
    if len(comments) > 50 :
        break
        
  return results["items"]
  
 
    
def get_





if __name__ == '__main__':
    
    #Perform Github tests
    #githubTest()
    
    
    #Define youtube API parameters
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    DEVELOPER_KEY = 'AIzaSyD4gc2e-6lPQYg_T-kq8l9gIPtitqVhM7o'

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    
    #Test obtaining comments
    sid = SentimentIntensityAnalyzer()
    videoComments = {}
    videoIds = pd.read_csv("USvideos.csv")["video_id"]
    for video_id in videoIds:
        try:
            comments = []
            video_comment_threads = get_comment_threads(youtube,  video_id,  comments)
            
            commentStats = {}
            
            for thread in video_comment_threads:
                #tic = time.time()
                
                topComment =  thread["snippet"]["topLevelComment"]
                text = topComment["snippet"]["textDisplay"]
                
                ss = sid.polarity_scores(text)['compound']
                
                #print( "Comment: %s" % (text))
                #print("Sentiment: %s\n" % str(ss) )
                
                commentStats[text] = getCommentStats(text)
                
                
                comments = get_comments(youtube, thread["id"], comments)
                for comment in comments:
                    text = comment["snippet"]["textDisplay"]
                    ss = sid.polarity_scores(text)['compound']
                    print( "Comment: %s" % (text))
                    print("Sentiment: %s\n" % str(ss) )
                    
                    commentSentiments[text] = ss
                    #print( "Comment by %s: %s" % (author, text))
                    #print(time.time() - tic)
        
        
        except HttpError:
            print ("An HTTP error occurred")
        
        videoComments[video_id] = commentSentiments
        
        
    
    
 