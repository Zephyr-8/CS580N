import login
import subreddit
import comments
import requests
import json
import time
import datetime
import sys
import pymongo
from pymongo import MongoClient


def OuathMaintainer(username, password):
    """
    Update Ouath2 head
    """
    code,Ouath2header = login.Ouath2(username, password)

    return code,Ouath2header


def FindJob(Ouath2header, db):
    """
    Check r/IAma new article
    """
    article = subreddit.CheckNew(Ouath2header,db)

    return article


def Issue(Ouath2header, postID, db):
    """
    Once find a new article call comments.py to grap all comments
    """
    comments.GetComments(Ouath2header, postID, "r/IAmA", db)


def FSM(index):
    """
    Sleeping time finite-state machine
    """
    if index in range(0,10):
        index=index+5
        print("Sleeping 300s")
        time.sleep(300)
        return index
    if index in range(10,50):
        index=index+25
        print("Sleeping 900s")
        time.sleep(900)
        return index
    if index in range(50,161):
        index=index+50
        print("Sleeping 3600s")
        time.sleep(3600)
        return index
    if index>161:
        print("Sleeping 28800s")
        time.sleep(28800)
        index=0
        return index


def main():
    #print("Error! Using >$ python3 job_issuer.py <user name> <password>")
    client = MongoClient()
    db = client.reddT2
    sleep_index=0
    while True:
        code,Ouath2header = OuathMaintainer(sys.argv[1], sys.argv[2])
        if code==200:
            print("==================================================")
            article = FindJob(Ouath2header, db)
            print("%d articles need update    " % len(article),datetime.datetime.now())
            if article:
                sleep_index = sleep_index - len(article) * 5
                if sleep_index < 0:
                    sleep_index = 0
                for i in article:
                    print("Aticle: %s in processing..." % i)
                    try:
                        Issue(Ouath2header,i,db)
                    except:
                        print("Error when updating {0} in list {1}    ".format(i, article), datetime.datetime.now())
                print("Complete crawling comments    ",datetime.datetime.now())
            
            sleep_index = FSM(sleep_index)
        else:
            break

    print("Exit! with code:",code)


def ErrorRestore(postID):
    client = MongoClient()
    db = client.reddT2
    code,Ouath2header = OuathMaintainer(sys.argv[1], sys.argv[2])
    Issue(Ouath2header,postID,db)
    print("Restore Finish")


if __name__ == "__main__":
    #ErrorRestore()
    main()