import os
import glob
from pymongo import MongoClient

class reddit_usr:
  def __init__(self, subreddit, id,keywords):
    self.subreddit = subreddit
    self.id = id
    self.keywords = keywords
    self.file = open(pwd+'/result_Q4/result_' + self.id + '.txt', 'w')
  def check_relevance(self,tweet):
      str_keywords = ",".join(self.keywords)
      hit_amount = sum([1 if w in tweet and w else 0 for w in str_keywords.split(',')])
      if((hit_amount>len(self.keywords)*0.5) and (len(self.keywords)>2)):
          return True
      else:
          return False




def copy_elimination(origin):
    output = []
    for i in origin:
        if not i in output:
            output.append(i)
    return output


def get_each_usr(filepath):
    f = open(filepath)
    line = 'not empty'
    reddit_usr_list = []
    while line:
        line = f.readline()
        line = line.rstrip('\n')
        reddit_usr_list.append(line)
    f.close()
    del reddit_usr_list[-1]
    new = reddit_usr_list[0].rpartition('/')
    del reddit_usr_list[0]
    cpy_elim_list = copy_elimination(reddit_usr_list)
    reddit_user = reddit_usr(new[0], new[2], cpy_elim_list)
    return reddit_user

def get_reddit_list(filedir):
    txt_list = glob.glob(filedir + '/' + '*.txt')
    txt_num = len(txt_list)
    reddit_list = []
    for i in range(txt_num):
        reddit_list.append(get_each_usr(txt_list[i]))
    return reddit_list

def _connect_mongo(host, port, db):
    conn = MongoClient(host, port)
    return conn[db]



if __name__ == '__main__':
    pwd = os.getcwd()
    dirname = pwd + '/result_Q4'
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    filedir = pwd + '/keywords1'
    reddit_list = get_reddit_list(filedir)
    f = open(pwd+'/result_index.txt',mode='w')
    db = _connect_mongo('localhost',27017,'twitter_db')
    cursor = db['twitter_collection'].find({},{'_id':0,'tweet_id':1,'text':1})
    while True:
        try:
            thisdoc = cursor.next()
        except:
            break
        for reddit in reddit_list:
            flag = reddit.check_relevance(thisdoc['text'])
            if(flag == True):
                print(thisdoc['tweet_id'],'hit!',file=f)
                print(thisdoc['tweet_id'],end='\n',file=reddit.file)
        continue

        
    f.close()
    for reddit in reddit_list:
        reddit.file.close()









