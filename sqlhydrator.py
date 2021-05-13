import Database # a python file used for database authentication with the mysql connector
from datetime import datetime
from twarc import Twarc
import json
import os
import atexit
import mysql.connector
from mysql.connector import errorcode

# twitter credentials
ck =
cs =
act =
acts =

FOLDERTOFILTER = "/COVID-19-TweetIDs-master/filename"

# ID is the tweet id, line is line in file, can be used as a sanity check/easier to track the file lines
lastProcessedId = 0
lastProcessedLine = 0

# connect to database
database, cursor = Database.connect()

# connect to twarc
t = Twarc(ck, cs, act, acts, tweet_mode='extended')

# set up the query: insert into [table] (columns,...) values (placeholders,...);

query = """
INSERT INTO tweets (tweetid, userid, text, created_at, entities, language, retweet_id, retweet_userid, conversation_id) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""

# tuble of the values to insert into the database (in order of the columns above)


tweetid = 0
userid = 0
text = ""
# this is a default bc i have to initialize this
dtime = 'Thu Jan 01 00:00:00 +0000 2015'
created_at = datetime.strftime(datetime.strptime(dtime, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
entities = ""
lang = ""
rtid = None
rtuserid = None
convid = None


valuesToInsert = (
    tweetid,
    userid,
    text,
    created_at,
    entities,
    lang,
    rtid,
    rtuserid,
    convid
)

for entry in os.scandir(FOLDERTOFILTER):
    for tweet in t.hydrate(open(entry)):
        logfile = open(entry.name + "-full-tweet.txt", 'a')
        # outtext logic is from the old hydrator
        tweet["display_text_range"] = [0, 280]
        outtext = ''
        logfile.write(json.dumps(tweet) + '\n')

        if 'retweeted_status' in tweet.keys():
            # getting tweet content
            outtext = tweet["retweeted_status"]['full_text'].encode('UTF-8', 'xmlcharrefreplace')
            # outtext = tweet['full_text'].encode('UTF-8', 'xmlcharrefreplace')
            outtext = "'" + outtext.decode().replace('\n', '   ') + "'"
            rtid = tweet['retweeted_status']['id']
            rtuserid = tweet['retweeted_status']['user']['id']


        # THIS GETS RETWEET TEXT, THEN GET ANYTHING IN THE POTNETIAL QUOTE TWEET

        else:
            outtext = tweet['full_text'].encode('UTF-8', 'xmlcharrefreplace')
            outtext = "'" + outtext.decode().replace('\n', '   ') + "'"

        tweetid = tweet['id']
        userid = tweet['user']['id']
        text = outtext
        dtime = tweet['created_at']
        created_at = datetime.strftime(datetime.strptime(dtime, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
        entities = json.dumps(tweet['entities'])
        lang = tweet['lang']

        #rtid and rtuserid defined in the retweeted status thing

        valuesToInsert = (
            tweetid,
            userid,
            text,
            created_at,
            entities,
            lang,
            rtid,
            rtuserid,
            convid
        )

        # update the last processed boiz
        lastProcessedId = tweet['id']
        lastProcessedLine += 1

        ## execute the query (can call this multiple times on the same query with different tuples)
        try:
            #passing if the query fails as the only inserts thatll be failing are the matching
            cursor.execute(query, valuesToInsert)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DUP_ENTRY:
                pass
            else:
                print(err)
                print('errnum ', err.errno)
    print(entry)
    lastProcessedLine = 0
# running this from slurm script so this will just get printed to the file


def printCrash():
    print(lastProcessedId)
    print(lastProcessedLine)

atexit.register(printCrash)
