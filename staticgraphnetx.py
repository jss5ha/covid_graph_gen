import networkx
import Database #file containing mysql authentication information
import json
import mysql.connector
from mysql.connector import errorcode
from networkx.algorithms import community
from networkx.readwrite import  gexf

getbounds = """select count(*) from masktweets where created_at between '2020/03/01' and '2020/03/08';"""
gettweets = """select * from masktweets where created_at between '2020/03/01' and '2020/03/08';"""

database, cursor = Database.connect()

dg= networkx.DiGraph()

cursor.execute(getbounds)
bound = cursor.fetchone()[0]

result = cursor.execute(gettweets)

print("bound",bound)

#figure out for loop bounds
for i in range(bound):
    tweet = cursor.fetchone()

    if tweet is None:
        break
    # userids work as node ids
    userid = tweet[1]
    entities = json.loads(tweet[4])
    rtuid = tweet[7]
    sentiment = tweet[9]



    # if rtid is null and mention is null then we are good to go to next tweet
    if (rtuid is None) and ('user_mentions' not in entities.keys()):
        continue

    #then we either add tweet node or update its contents
    if userid not in dg:
        dg.add_node(userid)
        dg.nodes[userid]['overallsentiment']=sentiment
        dg.nodes[userid]['numpost']=1
    elif userid in dg:
        #print(dg.nodes[userid]['numpost'])
        #print(dg.nodes[userid]['numpost'])
        curnumpost = dg.nodes[userid]['numpost']
        dg.nodes[userid]['numpost'] = dg.nodes[userid]['numpost'] + 1
        dg.nodes[userid]['overallsentiment'] = (dg.nodes[userid]['overallsentiment'] * curnumpost +sentiment)/dg.nodes[userid]['numpost']
    # getting the node ids for edges
    # entities will have ppl mentioned
    if 'user_mentions' in entities.keys():
        # get the mention ids
        for mention in entities['user_mentions']:
            # get the user id of whomstever mentioned
            menid = mention['id']
            #make mennode
            if menid not in dg:
                dg.add_node(menid)
                #0 init because the person is being tweeted at, this isnt their feelings
                dg.nodes[menid]['overallsentiment'] = 0.0
                #0 init bc theyre not tweeting
                dg.nodes[menid]['numpost'] = 0

            if not dg.has_edge(userid, menid):
                dg.add_edge(userid, menid, edgeoverallsentiment=sentiment, edgenumpost=1)
            # get edge, update sentiment
            else:
                curnumpost = dg[userid][menid]['edgenumpost']
                dg[userid][menid]['edgenumpost'] += 1
                dg[userid][menid]['edgeoverallsentiment'] = (dg[userid][menid]['edgeoverallsentiment'] * curnumpost + sentiment) / dg[userid][menid]['edgenumpost']

    # if rtuid is not null itll have whomever was rt'd
    if rtuid is not None:
        #make rtuid node

        if rtuid not in dg:
            dg.add_node(rtuid)
            dg.nodes[rtuid]['overallsentiment'] = sentiment
            dg.nodes[rtuid]['numpost'] = 1

        if not dg.has_edge(userid, rtuid):
            dg.add_edge(userid, rtuid, edgeoverallsentiment=sentiment, edgenumpost=1)
        # get edge, update sentiment
        else:
            curnumpost = dg[userid][rtuid]['edgenumpost']
            dg[userid][rtuid]['edgenumpost'] += 1
            dg[userid][rtuid]['edgeoverallsentiment'] = (dg[userid][rtuid]['edgeoverallsentiment']*curnumpost + sentiment) /dg[userid][rtuid]['edgenumpost']

#now we done with getting the grph together
#gives us a list of nodes, 1 in each communities
print('printin communities!')
#write graph out
gexf.write_gexf(dg, "graphbackupjun6.gexf")
"""communities = list(community.greedy_modularity_communities(networkx.Graph(dg)))
#print the top 6 in this guy
for i in range(0,6):
    #lets get the overall sentiments, as well as the most well connected users from these big communities
    topnodes = []
    smallestdegree = float('inf')
    comsenti = 0.0;
    comnumposts = 0;
    for node in communities[i]:
        comsenti += dg.nodes[node]['overallsentiment']
        comnumposts += dg.nodes[node]['numpost']
        if len(topnodes) < 10:
            topnodes.append(node)
        elif len(topnodes) == 10:
            for tnode in topnodes:
                if tnode < smallestdegree:
                    smallestdegree = tnode
        else:
            if node > smallestdegree:
                topnodes.remove(smallestdegree)
                topnodes.append(node)
                smallestdegree = node
                for tnode in topnodes:
                    if tnode < smallestdegree:
                        smallestdegree = tnode

    #get the average of everything here
    comsenti = comsenti/comnumposts

    print('community ', i, ' has overall sentiment (weighted avg) of ', comsenti)
    print('top nodes from community ', i)
    for nod in topnodes:
        print(nod)

print('communities printed')"""
