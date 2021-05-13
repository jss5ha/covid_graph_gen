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

    for tag in tagsforgraph:
        if tag != tagsforgraph[0]:
            if not (g.has_edge(tag, tagsforgraph[0])):
                g.add_edge(tag, tagsforgraph[0], cooccuringtweets=1)
            else:
                g[tag][tagsforgraph[0]]['cooccuringtweets']+=1

print('making backup')
gexf.write_gexf(g, "coccurrencegraphbackupjun6.gexf")

topedges = []
i = 0
low = float('inf')
for tag, tag2, attr in g.edges(data=True):
    if i < 30:
        topedges.append((tag,tag2,attr))
    elif i==30:
        for edge in topedges:
             if edge[2]['cooccuringtweets'] < low:
                 low = edge[2]['cooccuringtweets']
    else:
        if attr['cooccuringtweets'] >= low:
            for edge in topedges:
                if edge[2]['cooccuringtweets'] == low:
                    topedges.remove(edge)
                    break
            topedges.append((tag,tag2,attr))
            low = attr['cooccuringtweets']
            for thing in topedges:
                if thing[2]['cooccuringtweets'] < low:
                    low = thing[2]['cooccuringtweets']

    i+=1

print(topedges)
