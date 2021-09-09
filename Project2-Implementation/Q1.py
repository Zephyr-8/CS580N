import csv
import Watson
import Q1_figure
import os
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def makedic(sourcelist):
    """
    make dictionery
    """
    dic0={}
    for word in sourcelist:
        dic0[word] = dic0.get(word, 0) + 1
    
    return dic0


def Q1GetCategory(authenticator):
    csvFile = open("fr1.csv", "r")
    reader = csv.reader(csvFile)
    text = []
    linenumber=0
    for item in reader: #subreddit, postID, text
        linenumber+=1
        if reader.line_num == 1:
            continue
        if linenumber % 10 == 0:
            print("Processing...Finished {} posts, need stop for 3s.".format(linenumber))
            time.sleep(3)
        postID = item[1]
        subreddit = item[0]
        text = item[2]
        result = Watson.GetWatsonCategries(text,subreddit,postID,authenticator)
        if result:
            pass
        else:
            result = ">>>Try get reddit flag" + subreddit + "/" + postID
        calculate(result)

    csvFile.close()
    print("Get all {} posts' category.".format(linenumber))
    exportcsv()


def calculate(result):
    """
    write all key words to Q1result.txt
    """
    with open("Q1result.txt","a+") as f:
        f.writelines(result)
        f.write('\n')


def exportcsv():
    """
    export frequency to csv files
    """
    print("Exprt frequency to csv files.")
    Q1L1=[]
    for line in open("Q1result.txt"):
        line=line.replace("\n", '')
        x=line.split("/")
        Q1L1.append(x[1])

    category=makedic(Q1L1)
    with open("Q1L1.csv",'w',encoding='utf8',newline='') as f:
        w = csv.writer(f)
        w.writerows(category.items())

    L = sorted(category.items(),key=lambda item:item[1],reverse=True)
    L = L[:4]
    top4=[]
    for i in L:
        top4.append(i[0])

    T0=[]
    T1=[]
    T2=[]
    T3=[]
    for line in open("Q1result.txt"):
        line=line.replace("\n", '')
        x=line.split("/")
        if x[1] == top4[0]:
            if len(x) > 2:
                T0.append(x[2])
            else:
                T0.append("undefined")
        if x[1] == top4[1]:
            if len(x) > 2:
                T1.append(x[2])
            else:
                T1.append("undefined")
        if x[1] == top4[2]:
            if len(x) > 2:
                T2.append(x[2])
            else:
                T2.append("undefined")
        if x[1] == top4[3]:
            if len(x) > 2:
                T3.append(x[2])
            else:
                T3.append("undefined")

    category0=makedic(T0)
    category1=makedic(T1)
    category2=makedic(T2)
    category3=makedic(T3)

    index=0
    for i in top4:
        outfile = "/category/" + i + ".csv"
        path=os.path.abspath('.')
        path = path + outfile
        with open(path,'w',encoding='utf8',newline='') as f:
            w = csv.writer(f)
            if index == 0:
                w.writerows(category0.items())
            if index == 1:
                w.writerows(category1.items())
            if index == 2:
                w.writerows(category2.items())
            if index == 3:
                w.writerows(category3.items())
            index+=1
    draw()


def draw():
    """
    Draw plot
    """
    print("Draw plot.")
    Q1_figure.draw()


if __name__ == "__main__":
    key="DS-mbwwNwqAXVGJONGbzokI5Z6Y_YhDlfzKUKIgYGu-A"
    authenticator = Watson.GetAuthenticator(key)
    Q1GetCategory(authenticator)