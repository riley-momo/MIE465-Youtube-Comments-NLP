import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import string
import statistics
import operator
import seaborn as sn



from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


def getRandomForestImportance(X,clf):
    d = {}
    for feat, importance in zip(X.columns, clf.feature_importances_):
        d[feat] = importance
    d = sorted(d.items(), key=operator.itemgetter(1))
    top10 = d[-10:]
    for i in range(10):
        print(top10[i])



if __name__ == '__main__':
    #read data
    path = os.getcwd() + '\\video_csvs\\'
    data = pd.read_csv(path + "videoCommentStats.csv")
    categories = pd.read_csv("USvideos.csv")[ ['video_id','category_id']]
    #remove duplicates from categories
    categories.drop_duplicates(subset=None,keep='first',inplace=True)
    #join target to features
    data = pd.merge(data,categories,on='video_id',how='inner')
    #remove infrequent categories
    data = data[ (data['category_id'] != 43) & (data['category_id'] != 1) & (data['category_id'] != 2) & (data['category_id'] != 15) & (data['category_id'] != 19) & (data['category_id'] != 20) & (data['category_id'] != 27) & (data['category_id'] != 29) ]
    #undersample category 24
    sampleSize = sum(data['category_id'] == 24) - sum(data['category_id'] == 26)
    indices = data[ (data['category_id'] == 24) ].index
    randomIndices = np.random.choice(indices, sampleSize, replace = False)
    data = data.drop(randomIndices, axis=0)
    #undersample category 10
    sampleSize = sum(data['category_id'] == 10) - sum(data['category_id'] == 26)
    indices = data[ (data['category_id'] == 10) ].index
    randomIndices = np.random.choice(indices, sampleSize, replace = False)
    data = data.drop(randomIndices, axis=0)
    #split into training and testing sets
    train,test = train_test_split(data, test_size = 0.2)
    
    #create  model
    X = train.drop(['category_id','video_id'], axis = 1)
    #X = train[ ['meanSentiment','sentimentStdev','meanWordCount','wordCountStdev'] ]
    Y = train['category_id']
    
    #Init Model
    clf = LogisticRegression(C= 0.001)
    #fit model
    clf.fit(X,Y)
    #summarize feature importance
    #getRandomForestImportance(X,clf)
    feature_names = data.columns.values
    i=0
    #create category labels
    labels = ['Music','Sports', 'People & Blogs', 'Comedy', 'Entertainment', 'News & Politics', 'Howto & Style', 'Science & Technology']
    #get 10 most prominent features for each category
    for category in labels:
        top10 = np.argsort(clf.coef_[i])[-10:]
        print("%s: %s" % (category," ".join(feature_names[k] for k in top10)))
        i+=1
    #predict on testing set
    X = test.drop(['category_id','video_id'], axis = 1)
    preds = clf.predict(X)
    #get performance of model
    Y = test['category_id']
    #get accuracy score
    score = accuracy_score(Y,preds)
    print(score)
   
    #get classification report
    print(classification_report(Y, preds, target_names = labels ) )    
    #get confusion matrix, display as heatmap
    matrix = confusion_matrix(Y,preds)
    df = pd.DataFrame(matrix, index = labels, columns = labels)
    plt.figure(figsize = (10,7))
    sn.set(font_scale = 0.6)
    sn.heatmap(df, annot = True, annot_kws={"size":13}, cmap = "Blues")
    plt.ylabel('True Category')
    plt.xlabel('Actual Category')
    plt.title('YouTube Category Classification Confusion Matrix')
    plt.show()