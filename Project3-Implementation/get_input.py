import re
from flask import Flask, render_template,url_for,request
import time
import csv
import json
import base64
import ppp
from scripts import ltz
app = Flask(__name__)

def return_img_stream(img_local_path):
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream
 
def hello_world():
    img_path = './static/Q2.png'
    img_stream = return_img_stream(img_path)
    return render_template('showpic.html', img_stream=img_stream)

@app.route('/')
def my_form():
	img_path = './static/Q2.png'
	img_stream = ppp.return_img_stream(img_path)
	with open('./static/Q1L1.csv') as csv_file:
		data = csv.reader(csv_file, delimiter=',')
		first_line = True
		ssslabel = []
		sssdata = []
		for row in data:
			if not first_line:
				ssslabel.append(row[0].replace(",", ""))
				sssdata.append(int(row[1]))
			else:
				first_line = False
	return render_template('nav.html', ssslabel=ssslabel, sssdata=sssdata,img_stream=img_stream )
	#return render_template('nav.html')

@app.route('/nav.html')
def goto_nav():
	img_path = './static/Q2.png'
	img_stream = ppp.return_img_stream(img_path)
	with open('./static/Q1L1.csv') as csv_file:
		data = csv.reader(csv_file, delimiter=',')
		first_line = True
		ssslabel = []
		sssdata = []
		for row in data:
			if not first_line:
				ssslabel.append(row[0].replace(",", ""))
				sssdata.append(int(row[1]))
			else:
				first_line = False
	return render_template('nav.html', ssslabel=ssslabel, sssdata=sssdata,img_stream=img_stream)

@app.route('/csv-dataset.html')
def go_to_categories():
	TTT= []
	with open('./static/Q1_time.txt') as timeline:
		for line in timeline:
			TTT.append(line)
	last_start_time = TTT[0]
	last_end_time = TTT[1]
	with open('./static/Q1_new.csv') as csv_file:
		data = csv.reader(csv_file, delimiter=',')
		first_line = True
		ssslabel = []
		sssdata = []
		for row in data:
			if not first_line:
				ssslabel.append(row[0].replace(",", ""))
				sssdata.append(int(row[1]))
			else:
				first_line = False
	return render_template('csv-dataset.html', ssslabel=ssslabel, sssdata=sssdata, last_start_time= last_start_time, last_end_time=last_end_time)

@app.route('/csv-dataset.html',methods=['GET', 'POST'])
def input_categories():
	start_time = request.form['start_time']
	end_time=request.form['end_time']
	q=1
	print(start_time)
	print(end_time)
	if re.match(r"\d{4}-\d{2}-\d{2}", start_time) and re.match(r"\d{4}-\d{2}-\d{2}", end_time):
		print(start_time)
		print(end_time)
		#call function to generate csv at here
		ltz.get_csv(q,start_time,end_time)
		#time.sleep(40)
		with open('./static/Q1_new.csv') as csv_file:
			data = csv.reader(csv_file, delimiter=',')
			first_line = True
			ssslabel = []
			sssdata = []
			for row in data:
				if not first_line:
					ssslabel.append(row[0].replace(",", ""))
					sssdata.append(int(row[1]))
				else:
					first_line = False

		return render_template('csv-dataset.html',ssslabel=ssslabel, sssdata=sssdata)
	else:
		return "Date format is not correct!"
	#return render_template('csv-dataset.html')

@app.route('/showpic.html')
def go_to_word():
	TTT= []
	with open('./static/Q1_time.txt') as timeline:
		for line in timeline:
			TTT.append(line)
	last_start_time = TTT[0]
	last_end_time = TTT[1]
	img_path = './static/Q2_new.png'
	img_stream = ppp.return_img_stream(img_path)
	return render_template('showpic.html',img_stream=img_stream,last_start_time= last_start_time, last_end_time=last_end_time)

@app.route('/showpic.html',methods=['GET', 'POST'])
def input_word():
	start_time = request.form['start_time']
	end_time=request.form['end_time']
	q=2
	print(start_time)
	print(end_time)
	if re.match(r"\d{4}-\d{2}-\d{2}", start_time) and re.match(r"\d{4}-\d{2}-\d{2}", end_time):
		print(start_time)
		print(end_time)
		ltz.get_csv(q,start_time,end_time)
		#call function to generate csv at here
		
		#time.sleep(40)
		img_path = './static/Q2_new.png'
		img_stream = ppp.return_img_stream(img_path)
		
		return render_template('showpic.html', img_stream=img_stream)
	else:
		return "Date format is not correct!"

if __name__ == '__main__':
	#app.run(debug=True, port=5000)
	app.run(host='0.0.0.0', port=5000)