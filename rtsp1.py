import rtsp
import datetime

RTSP_URL = "rtsp://..."
IMAGE_COUNT = 10

client = rtsp.Client(rtsp_server_uri = RTSP_URL)
while client.isOpened() and IMAGE_COUNT > 0:
    client.read().save("./"+ str(datetime.datetime.now()) +".jpg")
    IMAGE_COUNT = IMAGE_COUNT - 1
client.close()