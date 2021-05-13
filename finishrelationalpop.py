import Database
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
getsometweets = """select * from tweets limit 113078999, 113192191;"""

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
'''
for i in range (0,1001):
    print(i)
    check if its the remainder case
    if i == 1000:
        start = laststart
        limit = rownum

    #select errything
    cursor.execute(getsometweets, (start, limit))
    for i in range(0,113192):
'''
cursor.execute(getsometweets)
#gotta loop thru all them tweets tho
#gets us all the info from each row
for i in range (laststart, rownum):
    tweet = cursor.fetchone()


    tweetid = tweet[0]
    #turn it into a dict
    entities = json.loads(tweet[4])
    
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