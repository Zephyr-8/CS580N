from datetime import datetime,timedelta
from pymongo import MongoClient
import tzlocal
import matplotlib.pyplot as plt
import numpy as np
import collections
import calendar


def weekday_count(start_date, end_date):
	week={}
	for i in range((end_date - start_date).days):
		day = calendar.day_name[(start_date + timedelta(days=i+1)).weekday()]
		week[day] = week[day] + 1 if day in week else 1
	return week

def get_time(collection):
	time_count=[[0 for i in range(7)] for j in range(24)]
	time_weekdays=[]
	time_hours=[]
	max_timestamp=0
	min_timestamp=1606521600
	for doc in collection.find():
		time_stamp=doc['time_stamp']
		if time_stamp>1603256400:
			min_timestamp=min(time_stamp,min_timestamp)
			max_timestamp=max(time_stamp,max_timestamp)
			local_time=datetime.fromtimestamp(time_stamp)
			weekday=local_time.weekday()
			hour=local_time.hour
			time_weekdays.append(weekday)
			time_hours.append(hour)
			time_count[hour][weekday]+=1

	start_date=datetime.fromtimestamp(min_timestamp)
	start_date=start_date-timedelta(days=1)
	end_date=datetime.fromtimestamp(max_timestamp)
	weekdays_num=weekday_count(start_date,end_date)
	

	print(time_weekdays,time_hours,len(time_weekdays),len(time_hours))
	#print(time_count)
	print(weekdays_num)
	print(end_date)
	print(start_date)
	return time_count,time_weekdays,time_hours,weekdays_num

def plot_map(weekdays_counter):
	data_count=[[191, 25, 34, 41, 16, 32, 12], 
				[185, 19, 21, 25, 17, 29, 9], 
				[124, 29, 15, 22, 13, 21, 12], 
				[118, 21, 22, 26, 15, 26, 13], 
				[86, 12, 9, 19, 10, 20, 7], 
				[83, 11, 14, 31, 14, 19, 9], 
				[82, 18, 17, 24, 16, 21, 9], 
				[97, 33, 53, 60, 17, 27, 7], 
				[136, 27, 97, 89, 29, 28, 14], 
				[123, 57, 100, 91, 54, 25, 11], 
				[137, 66, 158, 84, 153, 33, 17], 
				[88, 204, 162, 120, 328, 22, 9], 
				[87, 237, 575, 145, 337, 91, 16], 
				[80, 209, 484, 184, 434, 84, 19], 
				[153, 190, 309, 192, 270, 42, 89], 
				[949, 142, 235, 114, 146, 61, 54], 
				[275, 127, 169, 81, 116, 63, 115], 
				[218, 98, 133, 872, 97, 41, 122], 
				[179, 55, 146, 1337, 53, 37, 309], 
				[140, 55, 82, 280, 49, 35, 237], 
				[72, 51, 77, 42, 31, 27, 227], 
				[61, 32, 53, 28, 41, 24, 204], 
				[51, 41, 48, 33, 34, 32, 289], 
				[30, 39, 45, 22, 45, 20, 258]]

	vector=[weekdays_counter['Monday'],weekdays_counter['Tuesday'],weekdays_counter['Wednesday'],weekdays_counter['Thursday'],weekdays_counter['Friday'],weekdays_counter['Saturday'],weekdays_counter['Sunday']]

	data_count=np.array(data_count)
	vector=np.array(vector)
	print(vector)
	normalized_data=[]
	for row in data_count:
		row=row/vector
		normalized_data.append(row)
	print(normalized_data)
	x=[0,1,2,3,4,5,6,7]
	y=[i+1 for i in range(-1,24)]
	x,y=np.meshgrid(x,y)
	plt.pcolormesh(x,y,normalized_data)
	plt.colorbar()
	plt.grid(True)
	plt.title("IAmA Comments Traffic Analysis")
	plt.xlabel("Weekdays from Monday to Sunday")
	plt.ylabel("From 00:00 to 23:59")
	plt.savefig("IAmA_time.pdf")

def main():
	client = MongoClient('localhost',27017)
	db=client.reddT2
	collection=db.comments
	time_count,time_weekdays,time_hours,weekdays_counter=get_time(collection)
	count=0
	for week in time_count:
		count+=sum(week)
	print(count)
	plot_map(weekdays_counter)

if __name__=="__main__":
	main()