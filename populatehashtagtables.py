import Database #file containing mysql authentication information
import json
import os
import atexit
import mysql.connector
from mysql.connector import errorcode

getsometweets = """select * from tweets;"""

sellastinsert = """select last_insert_id();"""

hashtagsvaltoinsert = ()
tweethashtagvalstoinsert = ()

#id to hashtag
insertintohashtags = """insert into hashtags (hashtag) VALUES (%s);"""

#tweet to hashtag(s)
insertintotweethashtags = """insert into tweet_hashtag (tweetid, hashtagid) VALUES (%s, %s);"""

database, cursor = Database.connect()
database2, _ = Database.connect()
cursor2 = database2.cursor(buffered=True)
database3, _ = Database.connect()
cursor3 = database3.cursor(buffered=True)
database4, cursor4 = Database.connect()


cursor.execute(getsometweets)
#gotta loop thru all them tweets tho
#gets us all the info from each row
for i in range (0,113192191):
    tweet = cursor.fetchone()

    tweetid = tweet[0]
    # turn it into a dict
    entities = json.loads(tweet[4])
    
    # content for hashtags
    # only wanna put stuff in if there are hashtags

    if 'hashtags' in entities.keys():
        for hashtag in entities['hashtags']:
            # try to insert, if we cant its nbd
            #checking if list has hashtags


            try:
                # passing if the query fails as the only inserts thatll be failing are the matching
                hashtagsvaltoinsert = (hashtag['text'],)
                print("hash to put in ", hashtagsvaltoinsert)
                print("type of the hashtag to put in ", type(hashtag['text']))
                cursor2.execute(insertintohashtags, hashtagsvaltoinsert)
                database2.commit()
                cursor2.execute((sellastinsert,))
                id  = cursor2.fetchone()
                tweethashtagvalstoinsert = (tweetid, id)
                cursor2.execute(insertintotweethashtags, tweethashtagvalstoinsert)
                database2.commit()

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_DUP_ENTRY:
                    #if duplicate then we look for the duplciate and update hte table
                    # cant execute until code above has so this is safe
                    # switch to where hashtags equal
                    # add index to the text field in the table

                    selecthashtags = """select * from hashtags where hashtag = \'"""
                    selecthashtags = selecthashtags + hashtag['text'] + """\'"""
                    cursor2.execute(selecthashtags)
                    idandtag = cursor2.fetchone()
                    tweethashtagvalstoinsert = (tweetid, idandtag[0])
                    cursor2.execute(insertintotweethashtags, tweethashtagvalstoinsert)
                    database2.commit()