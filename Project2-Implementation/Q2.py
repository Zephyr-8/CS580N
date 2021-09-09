import csv
import Azure
import os
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def removeS(result):
    """
    Remove "'s" in key words
    """
    removed=[]
    for line in result:
        line=line.replace("'s", '')
        line=line.replace("’s", '')
        line=line.replace("'S", '')
        line=line.replace("’S", '')
        removed.append(line)

    return removed


def removeDuplicate(result):
    """
    remove duplicate key words
    """
    T=[]
    for i in result:
        for j in i.split(" "):
            T.append(j)

    duplicate = {} 
    for key in T:         
        duplicate[key.lower()] = duplicate.get(key.lower(), 0) + 1 

    z = []
    for k, v in duplicate.items():
        if v>=3:
        # if a word shows more then 2 times in a post
            z.append(k)

    T=[]
    for i in result:
        k=''
        for j in i.split(" "):
            com=j.lower()
            if com not in z:
                k = k + ' ' + j
                k=k.strip()
        if k :
            T.append(k)

    for i in z:
        T.append(i)
        T.append(i)
    
    return T


def Q2GetKeyWords(client):
    csvFile = open("fr.csv", "r")
    reader = csv.reader(csvFile)
    text = []
    linenumber=0
    for item in reader: #postID, subreddit, text
        linenumber+=1
        if reader.line_num == 1:
            continue
        if linenumber % 10 == 0:
            print("Processing...Finished {} posts, need stop for 5s.".format(linenumber))
            time.sleep(5)
        postID = item[1]
        subreddit = item[0]
        text = [item[2]]
        result = removeDuplicate(removeS(Azure.GetAzureKeyWords(client,text,subreddit,postID)))
        calculate(result)
        writeback(postID,subreddit,result)

    csvFile.close()
    draw()


def writeback(postID,subreddit,result):
    """
    writeback key words for Q4
    """
    outfile = "/keywords1/" + postID + ".txt"

    path=os.path.abspath('.')
    path = path + outfile
    if os.path.exists(path):
        print("existing!! {}/{}".format(subreddit,postID))
    with open(path,"w") as f:
        f.write(subreddit+"/"+postID)
        f.write('\n')
        for i in result:
            f.writelines(i)
            f.write('\n')


def calculate(result):
    """
    write all key words to Q2result.txt
    """
    with open("Q2result1.txt","a+") as f:
        for i in result:
            f.writelines(i)
            f.write('\n')


def draw():
    """
    draw word cloud
    """
    f = open(u'Q2result1.txt','r').read()
    sw = ['amp', 'x200B', 'of']
    wordcloud = WordCloud(stopwords=sw,collocations=False, regexp=None).process_text(f)
    with open('Q2frequency.csv','w') as f:
        w = csv.writer(f)
        w.writerows(wordcloud.items())

    wordcloud = WordCloud(background_color="white", width=1000, height=1000, margin=2, max_words=100, relative_scaling=0.7, mode="RGBA").generate_from_frequencies(wordcloud)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    wordcloud.to_file('Q2.png')

if __name__ == "__main__":
    key = "8385f059169f4a7d9573da65771ac448"
    endpoint = "https://iama-text.cognitiveservices.azure.com/"
    client = Azure.authenticate_client(key,endpoint)
    Q2GetKeyWords(client)