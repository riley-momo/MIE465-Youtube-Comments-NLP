import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import string
import statistics
import operator



from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif

if __name__ == '__main__':
    #read data
    data = pd.read_csv("videoCommentStats.csv")
    categories = pd.read_csv("USvideos.csv")[ ['video_id','category_id']]
    #remove duplicates from categories
    categories.drop_duplicates(subset=None,keep='first',inplace=True)
    #join target to features
    data = pd.merge(data,categories,on='video_id',how='inner')
    
    #Perform k trials of model
    sum = 0
    k = 300
    for i in range(k):
        #split into training and testing sets
        train,test = train_test_split(data, test_size = 0.2)
        #create  model
        X = train.drop(['category_id','video_id'], axis = 1)
        #X = train[ ['meanSentiment','sentimentStdev','meanWordCount','wordCountStdev'] ]
        Y = train['category_id']
        #Init Model
        clf = SVC()
        #fit model
        clf.fit(X,Y)
        #summarize feature importance
        # d = {}
        # for feat, importance in zip(X.columns, clf.feature_importances_):
        #     d[feat] = importance
        # d = sorted(d.items(), key=operator.itemgetter(1))
        # top10 = d[-10:]
        # for i in range(10):
        #     print(top10[i])
        #predict on testing set
        X = test.drop(['category_id','video_id'], axis = 1)
        #X = test[ ['meanSentiment','sentimentStdev','meanWordCount','wordCountStdev'] ]
        preds = clf.predict(X)
        #get performance of model
        Y = test['category_id']
        score = accuracy_score(Y,preds)
        sum += score
    avg_score = sum/k
    print(avg_score)    