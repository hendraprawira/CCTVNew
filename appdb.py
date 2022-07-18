# Import necessary libraries
from flask import Flask, render_template, Response
import cv2
from detection import video_frame, gen_frames

# Initialize the Flask app
app = Flask(__name__)

camera1 = cv2.VideoCapture(0)

# camera2 = cv2.VideoCapture(
#     'rtsp://admin:f4tahkoM@192.168.18.17/Streaming/Channels/201')

# camera3 = cv2.VideoCapture(
#     'rtsp://admin:f4tahkoM@192.168.18.17/Streaming/Channels/301')


@app.route('/')
def index():
    return render_template('test.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/video_feed_2')
# def video_feed_2():
#     return Response(gen_frames2(camera2), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/video_feed_3')
# def video_feed_3():
#     return Response(gen_frames3(camera3), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
