from pymongo import MongoClient
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num


def get_tweet_data(collection,new_collection):
	f=open("time_stamp.txt","w")
	for doc in collection.find({'time_stamp':{"$gt":1605848400,"$lt":1606366800}}):
		data={'time_stamp':doc['time_stamp']}
		print(doc['time_stamp'])
		new_collection.insert_one(data)
		f.write(str(doc['time_stamp'])+"\n")
	f.close()

def time_count(time_collection):
	day_map={20:0,21:1,22:2,23:3,24:4,25:5}
	hour_count = np.zeros((6, 24))

	for time_stamp in time_collection.find():
		time_convert=datetime.fromtimestamp(time_stamp['time_stamp'])
		print(time_convert)
		hour_count[day_map[time_convert.day]][time_convert.hour]+=1
	print(hour_count)
	f=open("time_count.txt","w")
	f.write(str(hour_count))
	f.close()

def daterange(start_date, end_date):
    delta = timedelta(hours=1)
    while start_date < end_date:
        yield start_date
        start_date += delta


def plot():
	hour_count=[[155409,166248,201218,203800,167796,189858,151268,135677,141511,160880,159902,176463,192537,212144,224270,228174,199907,178097,162819,151711,145482,145339,147834,150249],
 				[145660,150502,152802,159083,147235,142778,130208,123072,130412,138674,148932,166790,183541,200291,208934,213729,183568,171701,155544,147055,142249,136859,136761,137609],
 				[137551,143278,147759,152406,144208,137818,139981,136849,143081,149601,161203,172214,186350,205163,215422,218835,189740,176111,163135,154418,147399,146112,145649,148284],
 				[157257,171751,208594,207169,172172,150393,136331,136751,141846,166671,166142,177975,196859,209372,219176,220903,191717,176718,162914,162490,149862,150468,155372,152191],
 				[144738,150890,151843,160217,137736,127099,127951,122581,131604,140937,154159,171257,190491,203810,230696,225103,202946,230489,222485,177185,158133,155547,162598,158222],
				[159324,158591,160068,169288,146174,135924,135947,131707,137423,148962,167003,185455,214425,223367,218074,232295,231877,205901,173082,162586,152217,154913,155536,153228]]
	print(hour_count[0][0])
	start_date=datetime(2020,11,20,00,00)
	end_date=datetime(2020,11,26,00,00)
	x_time=[]
	y_numbers=np.array(hour_count)
	y_flatten=y_numbers.flatten()
	print(y_flatten)
	for single_date in daterange(start_date, end_date):
		print(single_date.strftime("%m-%d %H:%M"))
		x_time.append(single_date.strftime("%m-%d %H:%M"))
	plt.xlabel('Hourly time range')
	plt.ylabel('Number of tweets')
	plt.plot(x_time,y_flatten)
	plt.xticks([x_time[0],x_time[48],x_time[96],x_time[143]])
	plt.title("Twitter Sample Stream")
	plt.savefig("twiiter_time.pdf")
	
def main():

	client = MongoClient('localhost',27017)
	db=client.twitter_db
	collection=db.twitter_timestamp
	#new_collection=db.twitter_timestamp
	#get_tweet_data(collection,new_collection)
	#time_count(collection)
	plot()



if __name__=="__main__":
	main()