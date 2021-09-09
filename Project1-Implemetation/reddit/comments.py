import login
import requests
import json
import time
import datetime
import pymongo
from pymongo import MongoClient

api_url = 'https://oauth.reddit.com'


def GetCommentsXpost(Ouath2header, postID, subReddit, db):
    param = {'depth':1}
    response = requests.get(api_url + '/' + subReddit+ '/comments/' + postID,
                                headers=Ouath2header,
                                params= param)
    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}    {}"
                        .format(response.status_code,
                        response.text,
                        datetime.datetime.now())
    )
    js = response.json()
    jsonappend = js[0]['data']['children'][0]['data']
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

        update_key = {
            'subreddit':jsonappend['subreddit_name_prefixed'], 
            'id': jsonappend['id']
            }

        exist = db.CrossPosts.find_one(update_key)
        if exist:
            if exist['comments']<submission['comments']:
                GetComments(Ouath2header, postID, subReddit, db)
                print("Xpost {} needs update comments list".format(jsonappend['id']))
            else:
                print("Exist article and do not need update")
                pass

        result = db.CrossPosts.update(update_key, submission, upsert=True)
        if result['updatedExisting'] == False:
            GetComments(Ouath2header, postID, subReddit, db)

    except:
        print("Xpost {} update error in {}"
                .format(jsonappend['id'],
                jsonappend['subreddit_name_prefixed']),
                datetime.datetime.now())



def GetComments(Ouath2header, postID, subReddit, db):
    #param = {'comment':"gadr6l4", 'limit': 50}
    param = {'depth':1}
    if subReddit == "r/IAmA":
        response = requests.get(api_url + '/r/IAmA/comments/' + postID,
                                headers=Ouath2header,
                                params= param)
    else:
        response = requests.get(api_url + '/' + subReddit+ '/comments/' + postID,
                                headers=Ouath2header,
                                params= param)
    if response.status_code != 200:
        raise Exception("Request returned an error: {} {}    {}"
                        .format(response.status_code,
                        response.text,
                        datetime.datetime.now())
    )
    #with open('./aaa.json', 'w') as f:
        #json.dump(response.json(),f)
    moreCommentlist=[]
    js = response.json()
    jspath = js[1]['data']['children']
    for i in jspath:
        if i['kind'] == "t1":
            try:
                sub = {
                    'subreddit': i['data']['subreddit_name_prefixed'],
                    'post_id': postID,
                    'comment_id': i['data']['id'],
                    'text': i['data']['body'],
                    'author': i['data']['author'],
                    'score': i['data']['score'],
                    'time_stamp': i['data']['created_utc']
                }
                db.comments.update({'subreddit': i['data']['subreddit_name_prefixed'],
                                    'post_id': postID,
                                    'comment_id': i['data']['id']},
                                    sub,
                                    upsert=True)
            except:
                print("Update error in {0}/{1}!  ".format(postID,i['data']['id']), datetime.datetime.now())
        if i['kind'] == "more":
            moreCommentlist = i['data']['children']
    if moreCommentlist:
        GetMoreComments(postID, subReddit, moreCommentlist, Ouath2header, db)


def GetMoreComments(postID,subReddit, commentlist, Ouath2header, db):
    """
    Comments may not able to show all in once
    """
    stopflag=0
    for i in commentlist:
        stopflag = stopflag + 1
        param = {'depth':1, 'comment':i}

        if stopflag%10 == 0:
            time.sleep(1)
        if stopflag%1000 == 0:
            time.sleep(10)
        #prevent too many request in once
            
        if subReddit == "r/IAmA":
            response = requests.get(api_url + '/r/IAmA/comments/' + postID,
                                        headers=Ouath2header,
                                        params= param)
        else:
            response = requests.get(api_url + '/' + subReddit+ '/comments/' + postID,
                                        headers=Ouath2header,
                                        params= param)

        if response.status_code != 200:
            raise Exception("Request returned an error: {} {}    {}"
                                .format(response.status_code,
                                response.text,
                                datetime.datetime.now())
        )
        js = response.json()
        jspath = js[1]['data']['children']

        if jspath:
            jspath = js[1]['data']['children'][0]['data']
            try:
                sub = {
                    'subreddit': jspath['subreddit_name_prefixed'],
                    'post_id': postID,
                    'comment_id': jspath['id'],
                    'text': jspath['body'],
                    'author': jspath['author'],
                    'score': jspath['score'],
                    'time_stamp': jspath['created_utc']
                }
                db.comments.update({'subreddit': jspath['subreddit_name_prefixed'],
                                    'post_id': postID,
                                    'comment_id': jspath['id']},
                                    sub,
                                    upsert=True)
            except:
                print("Update erroe in {0}/{1}!  ".format(postID,i), datetime.datetime.now())
        else:
        #Some comments were deleted
            #print("No comments in {0}/{1}".format(postID,i))
            pass
