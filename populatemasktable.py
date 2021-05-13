import Database #file containing mysql authentication information
import json
import os
import atexit
import mysql.connector
from mysql.connector import errorcode
import regex as re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer;


#nltk setup
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

#this passes the compound value to the sentiment its a normalized sentiment from -1 to 1
#-.5 > is negative, -.5 to .5 is neutral, .5 < is positive

#make my regex
maskpattern = re.compile('.*mask.*');

getsometweets = """select * from tweets;"""

query = """
INSERT INTO masktweets (tweetid, userid, text, created_at, entities, language, retweet_id, retweet_userid, conversation_id, sentiment) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""



database, cursor = Database.connect()
database2, cursor2 = Database.connect()

cursor.execute(getsometweets)
for i in range(0, 113192191):
    tweet = cursor.fetchone()

    #pull the text from the tweet
    tweettext = tweet[2]
    #if match push into the database
    mask = maskpattern.search(tweettext, re.IGNORECASE)
    if mask is not None:

        valuestoinsert = (
            tweet[0],
            tweet[1],
            tweet[2],
            tweet[3],
            tweet[4],
            tweet[5],
            tweet[6],
            tweet[7],
            tweet[8],
            sid.polarity_scores(tweettext)['compound']
        )

        cursor2.execute(query, valuestoinsert)