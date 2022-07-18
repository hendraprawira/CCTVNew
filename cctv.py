# import the necessary packages
import cv2
import numpy as np
import time

font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0
classes = []

# load yolo

def video_cctv(camera):
    ret, frame = camera.read()  # read the camera frame
    # frame = detect_video(frame) #for detection
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()

    return frame

def gen_cctv(camera):
    while True:
        frame = video_cctv(camera)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

