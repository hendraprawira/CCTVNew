# Import necessary libraries
from flask import Flask, render_template, Response,request, redirect, url_for
import cv2
from cctv import video_cctv, gen_cctv
from detection import video_frame, gen_frames
import sqlite3
# Initialize the Flask app
app = Flask(__name__)
camera = []
database = r"database.db"
camera1 = cv2.VideoCapture(
    'rtsp://admin:f4tahkoM@192.168.18.17/Streaming/Channels/102')

# camera2 = cv2.VideoCapture(
#     'rtsp://admin:f4tahkoM@192.168.18.17/Streaming/Channels/201')

# camera3 = cv2.VideoCapture(
#     'rtsp://admin:f4tahkoM@192.168.18.17/Streaming/Channels/301')


@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cctv")
    data = cur.fetchall()
    empty = ["1","1","1","1","1","1","1","1","1","1","1","1","1"]
    return render_template('index.html', data=data,empty=empty)
@app.route('/sortByWilayah', methods=['GET', 'POST'])
def sortByWilayah():
    wilayah = request.form.get('wilayah')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    if(wilayah == "Semua"):
        cur.execute("SELECT * FROM cctv")
        data = cur.fetchall()
        empty = ["1","1","1","1","1","1","1","1","1","1","1","1","1"]
        return render_template('index.html', data=data,empty=empty)
    else:
        cur.execute("SELECT * FROM cctv where address=? ",(wilayah,))
        data = cur.fetchall()
        empty = ["1","1","1","1","1","1","1","1","1","1","1","1","1"]
        return render_template('index.html', data=data,empty=empty)
    
@app.route('/processaddCCTV', methods=['GET', 'POST'])
def processaddCCTV():
    link = request.form.get('link')
    wilayah = request.form.get('wilayah')
    conn = sqlite3.connect('database.db')
    sql = ''' INSERT INTO cctv(cctv_link,address)
              VALUES(?,?) '''
    project = (link, wilayah);
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return redirect(url_for('index'))

@app.route('/video_feed/<id>')
def video_feed(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cctv WHERE id =?",id)
    data = cur.fetchall()
    data_2 = []
    for data2 in data:
        data_2.append(data2)
    camera = cv2.VideoCapture(data_2[0][1])
    return Response(gen_cctv(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cctv_detection/<id>')
def cctv_detection(id):
    return render_template('detection.html', id=id)

@app.route('/cctv_maps')
def cctv_maps():
    return render_template('cctvMaps.html')

@app.route('/video_detection/<id>')
def video_detection(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cctv WHERE id =?",id)
    data = cur.fetchall()
    data_2 = []
    for data2 in data:
        data_2.append(data2)
    camera = cv2.VideoCapture(data_2[0][1])
    return Response(gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/addChannelCCTV')
def addChannelCCTV():
    return render_template('addCCTV.html')


# @app.route('/video_feed_2')
# def video_feed_2():
#     return Response(gen_frames2(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/video_feed_3')
# def video_feed_3():
#     return Response(gen_frames3(camera3), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)

# conn = sqlite3.connect('database.db')
# cur = conn.cursor()
# cur.execute("SELECT * FROM cctv WHERE id LIKE 6")
# data = cur.fetchall()
# data_2 = []
# for data2 in data:
#     data_2.append(data2)
# print(data_2[0][1])