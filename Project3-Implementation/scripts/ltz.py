import pandas as pd
from pymongo import MongoClient
import time
import calendar
import os
import re
from scripts import Q1,Q2



def _connect_mongo(host, port, db):
    conn = MongoClient(host, port)
    return conn[db]

def read_mongo(db, collection, query=None,projection=None, host='localhost', port=27017):

    # Connect to MongoDB
    if query is None:
        query = {}
    if projection is None:
        projection = {}


    db = _connect_mongo(host=host, port=port, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query,projection)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))

    return df
def trans_csv(filedir,filename,df):
    final_path = filedir+'/'+filename+'.csv'
    df.to_csv(final_path,index=False)
    return final_path

def combine_csv(filedir,filename,csv_list):
    for i in csv_list:
        fr = open(i, 'rb').read()
        with open('combine.csv', 'ab') as f:
            f.write(fr)
    df = pd.read_csv('combine.csv', header=None)
    datalist = df.drop_duplicates()
    dest_dir = get_dir_csv(filedir)
    datalist.to_csv(dest_dir+'/'+filename+'.csv', index=False, header=False)
    pwd = os.getcwd()
    path = os.path.join(pwd, 'combine.csv')
    csv_list.append(path)
    for i in csv_list:
        os.remove(i)

##this func combines data with the same query and projection from two diff collections in one db into one csv##
def get_csv_from_mongo(db, collection1,collection2,query=None,projection=None, host='localhost', port=27017,filedir=os.getcwd(),filename='fr'):
    filedir = filedir + "/tmp"
    pwd = os.getcwd()
    df1 = read_mongo(db, collection1, query,projection)
    final_path1 = trans_csv(pwd, '1', df1)
    df2 = read_mongo(db, collection2, query,projection)
    final_path2= trans_csv(pwd, '2', df2)
    csv_list = [final_path1,final_path2]
    combine_csv(filedir, filename, csv_list)



def get_query(query,start_ts = None,end_ts = None):
    if (start_ts == None) and (end_ts == None):
        del query["time_stamp"]
    else:
        if(start_ts != None) and (end_ts != None):
            del query["time_stamp"]
            query.update({"$and":[{ "time_stamp":{"$gte":start_ts} },{"time_stamp":{"$lte":end_ts}}]})
        if start_ts == None:
            query["time_stamp"].update({"$lte": end_ts})
        if (end_ts == None):
            query["time_stamp"].update({"$gte":start_ts})

def get_timestamp(start_date = '',end_date = ''):
    start_ts = None
    end_ts = None
    if start_date != '':
        start_ts = calendar.timegm(time.gmtime(time.mktime(time.strptime(start_date + ' 00:00:00', "%Y-%m-%d %H:%M:%S"))))
    if end_date != '':
        end_ts = calendar.timegm(time.gmtime(time.mktime(time.strptime(end_date + ' 23:59:59', "%Y-%m-%d %H:%M:%S"))))
    return start_ts,end_ts


#############if label is 1 or 2, you can optionally specify start and end time to acquire correspondding plots#########
#############else, user's label is invalid###################
def get_csv(label, start_time = '', end_time = ''):
        query = {"comments": {"$gt": 2}, "time_stamp": {}}
        start_ts, end_ts = get_timestamp(start_time, end_time)
        get_query(query,start_ts, end_ts)
        if(label==1):
            #print(start_time,end_time)
            get_csv_from_mongo('reddT2', 'CrossPosts', 'IAmA', query, {"_id": 0, "subreddit": 1, "id": 1, "title": 1},
                               filename='fr1')
            filename = "./static/Q1_time.txt"
            with open(filename,"w") as f:
                    f.writelines(start_time)
                    f.writelines('\n')
                    f.writelines(end_time)
            f.close()
            Q1.callByCSV(get_dir_csv())
            return True
        if(label==2):
            get_csv_from_mongo('reddT2', 'CrossPosts', 'IAmA', query, {"_id": 0, "subreddit": 1, "id": 1, "text": 1},
                               filename='fr2')
            filename = "./static/Q2_time.txt"
            with open(filename,"w") as f:
                    f.writelines(start_time)
                    f.writelines('\n')
                    f.writelines(end_time)
            f.close()
            Q2.callByCSV(get_dir_csv())
            return True

        return False


def get_dir_csv(filedir ="./scripts"):
    dest_dir = re.sub('scripts', 'tmp', filedir)
    #dest_dir = dest_dir + "/tmp"
    print(dest_dir)
    #Q1.callByCSV(get_dir_csv())
    #Q2.callByCSV(get_dir_csv())
    return dest_dir








