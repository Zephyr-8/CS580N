import numpy as np
import matplotlib.pyplot as plt
import csv


def barchart1(bars1, labels, path, ylabel, title):
    ind = np.arange(len(labels)) 
    width = 0.6    
    fig,ax = plt.subplots(figsize=(8, 5))
    ax.bar(ind, bars1,width,color='#4993C6', edgecolor='#000000')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels,rotation=35, rotation_mode='anchor', ha='right')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    for item in ([ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(13)
    plt.tight_layout()
    plt.xlim([-1, len(labels)])
    fig.savefig(path, bbox_inches='tight')


def barchart2(bars1, labels, path, ylabel, title):
    ind = np.arange(len(labels)) 
    width = 0.6    
    fig,ax = plt.subplots(figsize=(5, 4))
    ax.bar(ind, bars1,width,color='#4993C6', edgecolor='#000000')
    ax.set_xticks(ind)
    ax.set_xticklabels(labels,rotation=35, rotation_mode='anchor', ha='right')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    for item in ([ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(13)
    plt.tight_layout()
    plt.xlim([-1, len(labels)])
    fig.savefig(path, bbox_inches='tight')


def draw():
    percs=[]
    subs=[]
    csvFile = open("Q1L1.csv", "r")
    reader = csv.reader(csvFile)
    for item in reader:
        percs.append(int(item[1]))
        subs.append(item[0])

    barchart1(percs, subs, './figure/Q1L1.pdf', 'num of posts', "IAmA topics")

    percs=[]
    subs=[]
    csvFile = open("./category/law, govt and politics.csv", "r")
    reader = csv.reader(csvFile)
    for item in reader:
        percs.append(int(item[1]))
        subs.append(item[0])
    barchart2(percs, subs, './figure/law, govt and politics.pdf', 'num of posts', "Topics under law, govt and politics")

    percs=[]
    subs=[]
    csvFile = open("./category/art and entertainment.csv", "r")
    reader = csv.reader(csvFile)
    for item in reader:
        percs.append(int(item[1]))
        subs.append(item[0])
    barchart2(percs, subs, './figure/art and entertainment.pdf', 'num of posts', "Topics under art and entertainment")

    percs=[]
    subs=[]
    csvFile = open("./category/health and fitness.csv", "r")
    reader = csv.reader(csvFile)
    for item in reader:
        percs.append(int(item[1]))
        subs.append(item[0])
    barchart2(percs, subs, './figure/health and fitness.pdf', 'num of posts', "Topics under health and fitness")

    percs=[]
    subs=[]
    csvFile = open("./category/society.csv", "r")
    reader = csv.reader(csvFile)
    for item in reader:
        percs.append(int(item[1]))
        subs.append(item[0])
    barchart2(percs, subs, './figure/society.pdf', 'num of posts', "Topics under society")

    print("DONE")
