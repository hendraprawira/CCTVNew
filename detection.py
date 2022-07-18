# import the necessary packages
import cv2
import numpy as np
import time

font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0
classes = []

# load yolo
net = cv2.dnn.readNet("yolo-coco/yolov4-tiny/yolov4-tiny.weights",
                      "yolo-coco/yolov4-tiny/yolov4-tiny.cfg")

with open("yolo-coco/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]


def video_frame(camera):
    ret, frame = camera.read()  # read the camera frame
    frame = detect_video(frame) #for detection
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()

    return frame


# def video_frame2(camera):
#     ret, frame = camera.read()  # read the camera frame
#     # frame = detect_video(frame)
#     ret, buffer = cv2.imencode('.jpg', frame)
#     frame = buffer.tobytes()

#     return frame


# def video_frame3(camera):
#     ret, frame = camera.read()  # read the camera frame
#     # frame = detect_video(frame)
#     ret, buffer = cv2.imencode('.jpg', frame)
#     frame = buffer.tobytes()

#     return frame


def detect_video(frame):
    global frame_id

    frame_id = frame_id + 1
    height, width, channels = frame.shape

    # detecting object
    blod = cv2.dnn.blobFromImage(
        frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blod)
    outs = net.forward(output_layers)

    # showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)

                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # print(len(boxes))
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    # print(indexes)
    number_objects_detected = len(boxes)

    count = 0
    for i in range(len(boxes)):
        if i in indexes:
            if classes[class_ids[i]] == "person":
                x, y, w, h = boxes[i]
                label = classes[class_ids[i]]
                confidence = confidences[i]
                # color = colors[i]
                count += 1

                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (0, 255, 0), thickness=1)
                cv2.putText(frame, label + " " + str(round(confidence, 2)),
                            (x, y - 10), font, 0.5, (0, 255, 0), 2)

    elapsed_time = time.time() - starting_time
    fps = frame_id / elapsed_time
    # cv2.putText(frame, "FPS: " + str(round(fps, 2)),
    #             (10, 50), font, 4, (0, 0, 0), 3)

    cv2.putText(frame, "Count: " + str(count), (30, height - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    frame = cv2.resize(frame, (1280, 720), fx=0, fy=0,
                       interpolation=cv2.INTER_CUBIC)

    return frame


def gen_frames(camera):
    while True:
        frame = video_frame(camera)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

