import login
import comments
import requests
import json
import datetime
import pymongo
from pymongo import MongoClient
import re 


api_url = 'https://oauth.reddit.com'


def ParsingURL(string): 
    return re.search('.*reddit.com/(.*)/comments/(.*?)/.*',string).groups()


def Xpost(Ouath2header, db, submission):
    info = ParsingURL(submission['text'])
    if info:
        print("Redirect to", info[0], info[1])
        comments.GetCommentsXpost(Ouath2header, info[1], info[0], db)
    else:
        print("Cannot get crosspost info!")


def CheckNew(Ouath2header,db):
    """
    Check r/IAmA new atricle
    """
    article = []
    param = {'limit': 25}
    response = requests.get(api_url + '/r/IAmA/new', headers=Ouath2header, params= param)
    #param = {'q':"crosspost", 'limit': 10, 'restrict_sr': True}
    #response = requests.get(api_url + '/r/IAmA/search', headers=Ouath2header, params= param)
    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}    {}".format(response.status_code, response.text, datetime.datetime.now())
    )
    #with open('./bbb.json', 'w') as f:
        #json.dump(response.json(),f)
    js = response.json()
    for i in range(js['data']['dist']):
        jsonappend = js['data']['children'][i]['data']
        try:
            submission = {
                'subreddit': jsonappend['subreddit_name_prefixed'],
                'id': jsonappend['id'],
                'title': jsonappend['title'],
                'flag': jsonappend['link_flair_text'],
                'author': jsonappend['author'],
                'text': jsonappend['selftext'],
                'score': jsonappend['score'],
                'comments': jsonappend['num_comments'],
                'time_stamp': jsonappend['created_utc'],
                'url': jsonappend['url']
            }

            if submission['flag'] == "Crosspost":
                print("Processing crosspost in r/IAmA", submission['id'])
                Xpost(Ouath2header, db, submission)
                continue
            update_key = {
                'subreddit':jsonappend['subreddit_name_prefixed'], 
                'id': jsonappend['id']
                }

            exist = db.IAmA.find_one(update_key)
            if exist:
                if exist['comments']<submission['comments']:
                    article.append(jsonappend['id'])
                    #print("Article {} needs update comments list".format(jsonappend['id']))
                else:
                    #print("Exist article and do not need update")
                    pass

            result = db.IAmA.update(update_key, submission, upsert=True)
            if result['updatedExisting'] == False:
                article.append(jsonappend['id'])

        except:
            print("Article {} update error in {}".format(jsonappend['id'], jsonappend['subreddit_name_prefixed']), datetime.datetime.now())
    
    return article