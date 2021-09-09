import csv
from scripts import Watson
import os
import time


def makedic(sourcelist):
    """
    make dictionery
    """
    dic0={}
    for word in sourcelist:
        dic0[word] = dic0.get(word, 0) + 1
    
    return dic0


def Q1GetCategory(authenticator, path123):
    print(path123)
    filename = str(path123) + "/fr1.csv"
    csvFile = open(filename, "r")
    reader = csv.reader(csvFile)
    text = []
    linenumber=0
    for item in reader: #subreddit, postID, text
        linenumber+=1
        if reader.line_num == 1:
            continue
        if linenumber % 10 == 0:
            print("Processing...Finished {} posts, need stop for 2s.".format(linenumber))
            time.sleep(2)
        postID = item[1]
        subreddit = item[0]
        text = item[2]
        result = Watson.GetWatsonCategries(text,subreddit,postID,authenticator)
        if result:
            pass
        else:
            result = "IBM Watson bad result"
        calculate(result, path123)

    csvFile.close()
    print("Get all {} posts' category.".format(linenumber))
    exportcsv(path123)


def calculate(result, path123):
    """
    write all key words to Q1result.txt
    """
    filename = str(path123) + "/Q1result.txt"
    with open(filename, "a+") as f:
        f.writelines(result)
        f.write('\n')
    f.close()


def exportcsv(path123):
    """
    export frequency to csv files
    """
    filename = str(path123) + "/Q1result.txt"
    pathd = "./static/Q1_new.csv"
    print("Exprt frequency to csv files.")
    Q1L1=[]
    for line in open(filename):
        line=line.replace("\n", '')
        if line=="IBM Watson bad result":
            Q1L1.append(line)
        else:
            x=line.split("/")
            Q1L1.append(x[1])

    category=makedic(Q1L1)
    with open(pathd,'w',encoding='utf8',newline='') as f:
        w = csv.writer(f)
        w.writerow(['Categories','Times'])
        w.writerows(category.items())
    os.remove(filename)

def callByCSV(path123):
    """
    docstring
    """
    key="DS-mbwwNwqAXVGJONGbzokI5Z6Y_YhDlfzKUKIgYGu-A"
    authenticator = Watson.GetAuthenticator(key)
    Q1GetCategory(authenticator, path123)

if __name__ == "__main__":
    key="DS-mbwwNwqAXVGJONGbzokI5Z6Y_YhDlfzKUKIgYGu-A"
    #authenticator = Watson.GetAuthenticator(key)
    #Q1GetCategory(authenticato)