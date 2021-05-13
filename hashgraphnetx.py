import networkx
import Database #file containing mysql authentication information
import json
import mysql.connector
from mysql.connector import errorcode
from networkx.algorithms import community
from networkx.readwrite import  gexf


#get the bounds, doing this table will get me my userids n stuff too
getbounds = """select count(*) from masktweets where created_at between '2020/03/01' and '2020/03/08';"""
gettweets = """select * from masktweets where created_at between '2020/03/01' and '2020/03/08';"""

gethashtagid = """select hashtagid from tweet_hashtag where tweetid = """
gethashtag = """select hashtag from hashtags where id = """

database, cursor = Database.connect()
#second cursor so I can have the loop behave correctly
database2, cursor2 = Database.connect()

g= networkx.Graph()

cursor.execute(getbounds)
bound = cursor.fetchone()[0]

result = cursor.execute(gettweets)

useridtoinsert = (0,)
hashidtoinsert = (0,)

for i in range(bound):
    tweet = cursor.fetchone()
    tweetid = tweet[0]
    userid = tweet[1]

    #tweetidtoinsert = (tweetid,)
    tweetidtoinsert = gethashtagid+str(tweetid)+ """;"""
    #cursor2.execute(gethashtagid, tweetidtoinsert)
    cursor2.execute(tweetidtoinsert)
    tagsintweet = cursor2.fetchall()

    tagsforgraph = []
    for tag in tagsintweet:
        #hashidtoinsert  = (tag[0],)
        hashidtoinsert = gethashtag+str(tag[0])+""";"""
        #cursor2.execute(gethashtag, hashidtoinsert)
        cursor2.execute(hashidtoinsert)
        hashtag = cursor2.fetchone()[0]
        tagsforgraph.append(hashtag)

    if not g.has_node(userid):
        g.add_node(userid, tweets=0)

    for tag in tagsforgraph:
        if g.has_node(tag):
            g.nodes[tag]["tweets"] += 1
        else:
            g.add_node(tag, tweets=1)

        if g.has_edge(userid, tag):
            g[userid][tag]["edgetweets"] += 1
        else:
            g.add_edge(userid,tag, edgetweets=1)

print('making backup now')
gexf.write_gexf(g, "hashgraphbackupjun6.gexf")

node2num = {}
numtweetslist = []
i = 0
low = float('inf')
for n in g:
    if i < 20:
        numtweetslist.append(g.nodes[n]['tweets'])
        node2num[n] = g.nodes[n]['tweets']
    elif i==20:
        for num in numtweetslist:
             if num < low:
                 low = num
    else:
        if g.nodes[n]['tweets'] >= low:
            numtweetslist.remove(low)
            for key in node2num:
                if node2num[key] == low:
                    node2num.pop(key)
                    break
            numtweetslist.append(g.nodes[n]['tweets'])
            low = g.nodes[n]['tweets']
            node2num[n] = g.nodes[n]['tweets']
            for num in numtweetslist:
                if num < low:
                    low = num

    i+=1

print(node2num)
