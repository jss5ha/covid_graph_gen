import Database #file containing mysql authentication information
import json
import os
import atexit
import mysql.connector
from mysql.connector import errorcode

#total rows
rownum = 113192191
limit = 113192
start = 0
laststart = 113078999

#getsometweets = """select * from tweets order by created_at limit %s, %s"""
getsometweets = """select * from tweets;"""

hashtagsvaltoinsert = ()
tweethashtagvalstoinsert = ()
rtvalstoinsert = ()
tweetmentionsvalstoinsert = ()

#id to hashtag
insertintohashtags = """insert into hashtags (hashtag) VALUES (%s);"""

#tweet to hashtag(s)
insertintotweethashtags = """insert into tweet_hashtag (tweetid, hashtagid) VALUES (%s, %s);"""

#ties rtid to the id or the retweeted tweet
insertintoretweet = """insert into retweet (tweetid, originalid) VALUES (%s, %s);"""

#tweet to mentions
insertintotweetmentions = """insert into mentions (tweetid, userid) VALUES (%s, %s)"""


database, cursor = Database.connect()
database2, cursor2 = Database.connect()
database3, cursor3 = Database.connect()
database4, cursor4 = Database.connect()
database5, cursor5 = Database.connect()

cursor.execute(getsometweets)
#gotta loop thru all them tweets tho
#gets us all the info from each row
for i in range (0,laststart):
    tweet = cursor.fetchone()


    tweetid = tweet[0]
    #turn it into a dict
    entities = json.loads(tweet[4])

    #content for hashtags
    #only wanna put stuff in if there are hashtags
    if 'hashtags' in entities.keys():
        for hashtag in entities['hashtags']:
            #try to insert, if we cant its nbd
            try:
                #passing if the query fails as the only inserts thatll be failing are the matching
                hashtagsvaltoinsert = (hashtag)
                cursor2.execute(insertintohashtags, hashtagsvaltoinsert)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_DUP_ENTRY:
                    pass
                else:
                    print(err)
                    print('errnum ', err.errno)

        #content for tweethashtags
        #cant execute until code above has so this is safe
        #switch to where hashtags equal
        #add index to the text field in the table
        selecthashtags = """select * from hashtags where hashtags contains \'%"""
        selecthashtags = selecthashtags + hashtag + """%\'"""
        idandtag = cursor3.execute(selecthashtags)
        tweethashtagvalstoinsert = (tweetid, idandtag[0])
        cursor2.execute(insertintotweethashtags, tweethashtagvalstoinsert)

    #content for retweet
    originalid = tweet[6]
    rtvalstoinsert = (tweetid, originalid)
    cursor4.execute(insertintoretweet, rtvalstoinsert)

    #content for mentions
    if 'user_mentions' in entities.keys():
        for mention in entities['user_mentions']:
            #im dumb theres a typo in line 91.
            #passing if the query fails as the only inserts thatll be failing are the matching
            tweetmentionsvalstoinsert = (tweetid, mention['id'])
            cursor5.execute(insertintotweetmentions, tweetmentionsvalstoinsert)
            #gotta loop thru everyone mentioned


    #increment the counters here
    #start = start + 113192
    #limit = limit + 113192