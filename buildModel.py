import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import string
import statistics



from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree


if __name__ == '__main__':
    #read data
    data = pd.read_csv("videoCommentStats.csv")
    categories = pd.read_csv("USvideos.csv")[ ['video_id','category_id']]
    #remove duplicates from categories
    categories.drop_duplicates(subset=None,keep='first',inplace=True)
    #join target to features
    data = pd.merge(data,categories,on='video_id',how='inner')
    
    #split into training and testing sets
    train,test = train_test_split(data, test_size = 0.3)
    #create  model
    #X = train.drop(['category_id','video_id'], axis = 1)
    X = train[ ['meanSentiment','sentimentStdev','meanWordCount','wordCountStdev'] ]
    Y = train['category_id']
    clf = tree.DecisionTreeClassifier()
    #fit regression model
    clf.fit(X,Y)
    #predict on testing set
    #X = test.drop(['category_id','video_id'], axis = 1)
    X = test[ ['meanSentiment','sentimentStdev','meanWordCount','wordCountStdev'] ]
    preds = clf.predict(X)
    #get performance of model
    Y = test['category_id']
    score = accuracy_score(Y,preds)
    print(score)