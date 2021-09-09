import pandas as pd
from pymongo import MongoClient
import os



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
    datalist.to_csv(filedir+'/'+filename+'.csv', index=False, header=False)
    pwd = os.getcwd()
    path = os.path.join(pwd, 'combine.csv')
    csv_list.append(path)
    for i in csv_list:
        os.remove(i)

##this func combines data with the same query and projection from two diff collections in one db into one csv##
def get_csv_from_mongo(db, collection1,collection2,query=None,projection=None, host='localhost', port=27017,filedir=os.getcwd(),filename='fr'):
    pwd = os.getcwd()
    df1 = read_mongo(db, collection1, query,projection)
    final_path1 = trans_csv(pwd, '1', df1)
    df2 = read_mongo(db, collection2, query,projection)
    final_path2= trans_csv(pwd, '2', df2)
    csv_list = [final_path1,final_path2]
    combine_csv(filedir, filename, csv_list)



if __name__ == '__main__':
    get_csv_from_mongo('reddT2','CrossPosts','IAmA',{"comments":{"$gt":2}},{"_id":0, "subreddit":1, "id":1, "title":1},filename='fr1')
    get_csv_from_mongo('reddT2','CrossPosts','IAmA', {"comments": {"$gt": 2}}, {"_id": 0, "subreddit": 1, "id": 1, "text": 1}, filename='fr2')









