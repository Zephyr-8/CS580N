from flask import Flask
from flask import render_template
import base64


app = Flask(__name__)
 
def return_img_stream(img_local_path):
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream
 
 
#@app.route('/')
def hello_world():
    img_path = './static/Q2.png'
    img_stream = return_img_stream(img_path)
    return render_template('showpic.html', img_stream=img_stream)
 
 
if __name__ == '__main__':
    #app.run(debug=True, port=5000)
    app.run(host='0.0.0.0', port=5000)