# Import necessary libraries
from flask import Flask, render_template, Response
import cv2
from cctv import video_cctv, gen_cctv
from detection import video_frame, gen_frames
import sqlite3
import socket,cv2, pickle,struct
# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/video_feed')
def video_feed():
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_ip = '192.168.18.28' # paste your server ip address here
    port = 9999
    client_socket.connect((host_ip,port)) # a tuple
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
	    while len(data) < payload_size:
		    packet = client_socket.recv(4*1024) # 4K
		    if not packet: break
		    data+=packet
	    packed_msg_size = data[:payload_size]
	    data = data[payload_size:]
	    msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	    while len(data) < msg_size:
		    data += client_socket.recv(4*1024)
	    frame_data = data[:msg_size]
	    data  = data[msg_size:]
	    frame = pickle.loads(frame_data)
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == "__main__":
    app.run(debug=True)