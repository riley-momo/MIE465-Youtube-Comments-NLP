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
import emoji

from collections import Counter

from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import TweetTokenizer
from nltk.probability import FreqDist
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import *

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#Profanity list
def profanityList():
    return [
'2g1c',
'2 girls 1 cup',
'acrotomophilia',
'anal',
'anilingus',
'anus',
'arsehole',
'ass',
'asshole',
'assmunch',
'auto erotic',
'autoerotic',
'babeland',
'baby batter',
'ball gag',
'ball gravy',
'ball kicking',
'ball licking',
'ball sack',
'ball sucking',
'bangbros',
'bareback',
'barely legal',
'barenaked',
'bastardo',
'bastinado',
'bbw',
'bdsm',
'beaver cleaver',
'beaver lips',
'bestiality',
'bi curious',
'big black',
'big breasts',
'big knockers',
'big tits',
'bimbos',
'birdlock',
'bitch',
'black cock',
'blonde action',
'blonde on blonde action',
'blow j',
'blow your l',
'blue waffle',
'blumpkin',
'bollocks',
'bondage',
'boner',
'boob',
'boobs',
'booty call',
'brown showers',
'brunette action',
'bukkake',
'bulldyke',
'bullet vibe',
'bung hole',
'bunghole',
'busty',
'butt',
'buttcheeks',
'butthole',
'camel toe',
'camgirl',
'camslut',
'camwhore',
'carpet muncher',
'carpetmuncher',
'chocolate rosebuds',
'circlejerk',
'cleveland steamer',
'clit',
'clitoris',
'clover clamps',
'clusterfuck',
'cock',
'cocks',
'coprolagnia',
'coprophilia',
'cornhole',
'cum',
'cumming',
'cunnilingus',
'cunt',
'darkie',
'date rape',
'daterape',
'deep throat',
'deepthroat',
'dick',
'dildo',
'dirty pillows',
'dirty sanchez',
'dog style',
'doggie style',
'doggiestyle',
'doggy style',
'doggystyle',
'dolcett',
'domination',
'dominatrix',
'dommes',
'donkey punch',
'double dong',
'double penetration',
'dp action',
'eat my ass',
'ecchi',
'ejaculation',
'erotic',
'erotism',
'escort',
'ethical slut',
'eunuch',
'faggot',
'fecal',
'felch',
'fellatio',
'feltch',
'female squirting',
'femdom',
'figging',
'fingering',
'fisting',
'foot fetish',
'footjob',
'frotting',
'fuck',
'fucking',
'fuck buttons',
'fudge packer',
'fudgepacker',
'futanari',
'g-spot',
'gang bang',
'gay sex',
'genitals',
'giant cock',
'girl on',
'girl on top',
'girls gone wild',
'goatcx',
'goatse',
'gokkun',
'golden shower',
'goo girl',
'goodpoop',
'goregasm',
'grope',
'group sex',
'guro',
'hand job',
'handjob',
'hard core',
'hardcore',
'hentai',
'homoerotic',
'honkey',
'hooker',
'hot chick',
'how to kill',
'how to murder',
'huge fat',
'humping',
'incest',
'intercourse',
'jack off',
'jail bait',
'jailbait',
'jerk off',
'jigaboo',
'jiggaboo',
'jiggerboo',
'jizz',
'juggs',
'kike',
'kinbaku',
'kinkster',
'kinky',
'knobbing',
'leather restraint',
'leather straight jacket',
'lemon party',
'lolita',
'lovemaking',
'make me come',
'male squirting',
'masturbate',
'menage a trois',
'milf',
'missionary position',
'motherfucker',
'mound of venus',
'mr hands',
'muff diver',
'muffdiving',
'nambla',
'nawashi',
'negro',
'neonazi',
'nig nog',
'nigga',
'nigger',
'nimphomania',
'nipple',
'nipples',
'nsfw images',
'nude',
'nudity',
'nympho',
'nymphomania',
'octopussy',
'omorashi',
'one cup two girls',
'one guy one jar',
'orgasm',
'orgy',
'paedophile',
'panties',
'panty',
'pedobear',
'pedophile',
'pegging',
'penis',
'phone sex',
'piece of shit',
'piss pig',
'pissing',
'pisspig',
'playboy',
'pleasure chest',
'pole smoker',
'ponyplay',
'poof',
'poop chute',
'poopchute',
'porn',
'porno',
'pornography',
'prince albert piercing',
'pthc',
'pubes',
'pussy',
'queaf',
'raghead',
'raging boner',
'rape',
'raping',
'rapist',
'rectum',
'reverse cowgirl',
'rimjob',
'rimming',
'rosy palm',
'rosy palm and her 5 sisters',
'rusty trombone',
's&m',
'sadism',
'scat',
'schlong',
'scissoring',
'semen',
'sex',
'sexo',
'sexy',
'shaved beaver',
'shaved pussy',
'shemale',
'shibari',
'shit',
'shota',
'shrimping',
'slanteye',
'slut',
'smut',
'snatch',
'snowballing',
'sodomize',
'sodomy',
'spic',
'spooge',
'spread legs',
'strap on',
'strapon',
'strappado',
'strip club',
'style doggy',
'suck',
'sucks',
'suicide girls',
'sultry women',
'swastika',
'swinger',
'tainted love',
'taste my',
'tea bagging',
'threesome',
'throating',
'tied up',
'tight white',
'tit',
'tits',
'titties',
'titty',
'tongue in a',
'topless',
'tosser',
'towelhead',
'tranny',
'tribadism',
'tub girl',
'tubgirl',
'tushy',
'twat',
'twink',
'twinkie',
'two girls one cup',
'undressing',
'upskirt',
'urethra play',
'urophilia',
'vagina',
'venus mound',
'vibrator',
'violet blue',
'violet wand',
'vorarephilia',
'voyeur',
'vulva',
'wank',
'wet dream',
'wetback',
'white power',
'women rapping',
'wrapping men',
'wrinkled starfish',
'xx',
'xxx',
'yaoi',
'yellow showers',
'yiffy',
'yiffer',
'zoophilia']

def getFeatures(comments):
    features = {}
    
    
    
    #Create frequency distribution for wordcounts of comments
    tokenizer = RegexpTokenizer(r'\w+')
    lengths = (len(tokenizer.tokenize(str(comment))) for comment in comments)
    wordCountDist = Counter(lengths)
    #give keys better names
    for key in wordCountDist:
        wordCountDist['wordCount' + str(key)] = wordCountDist.pop(key) 
    #append wordcount distribution to feature dictionary
    features.update(wordCountDist)
    #create combined text
    combinedText = ' '.join( [str(comment) for comment in comments])
    
    #find emoji frequency
    emojiSum = len(''.join(c for c in combinedText if c in emoji.UNICODE_EMOJI))
    numAlphaNumeric = sum(c.isdigit() for c in combinedText) + sum(c.isalpha() for c in combinedText)
    if (numAlphaNumeric):
        emojiFreq = emojiSum/(numAlphaNumeric + emojiSum)
        features['emojiFreq'] = emojiFreq
    
    #remove punctuation and garbage characters
    combinedText = ''.join(c for c in combinedText if c.isspace() or c.isalpha() or c.isdigit() or  c in emoji.UNICODE_EMOJI)
    
    
    #tokenize
    tokenizer = TweetTokenizer()
    tokens = tokenizer.tokenize(combinedText.lower())
    #convert to nltk Text
    words = nltk.Text(tokens)
    #Find lexical variety
    if len(words):
        lexicalVariety = len(set(words))/len(words)
        features['lexicalVariety'] = lexicalVariety
    #find profanity frequency
    profanity = profanityList()
    profanitySum = 0
    for p in profanity:
        profanitySum += combinedText.count(p)
    #get wordCount
    wordCount = len(words)
    if wordCount:
        profanityFreq = profanitySum/wordCount
        features['profanityFreq'] = profanityFreq
    
    
    
    #remove stopwords
    stop = set(stopwords.words('english'))
    words = [w for w in words if w not in stop]
    #Stem text 
    stemmer = PorterStemmer()
    stemmedText = [stemmer.stem(w) for w in words]
    
    
    #get frequency distribution
    fdist = FreqDist(words)
    #convert FreqDist to dictionary, only keep top 15 most common terms
    fdist = dict(fdist.most_common(15))
    #append FreqDist to features
    features.update(fdist)
    
    
    
   
    
    
    
    
    
    return features


    
    
    
    
    

if __name__ == '__main__':

    
    path = '\\\\SRVA\\Homes$\\moherril\\Documents\\Analytics in Action\\Project\\MI465-Youtube-Comments-NLP' + '\\video_csvs'
    
    df = pd.read_csv('\\\\SRVA\\Homes$\\moherril\\Documents\\Analytics in Action\\Project\\MI465-Youtube-Comments-NLP' + '\\US_category_id.json')
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
    #convert videoComments to dataframe
    videoCommentsDF = pd.DataFrame.from_dict(videoData, orient = 'index').fillna(0)
    #Convert dataframe to csv
    videoCommentsDF.to_csv(path + '\\videoCommentStats.csv')