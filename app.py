import enum
from turtle import color
from unittest import result
from flask import Flask, render_template, Response, jsonify
import cv2
import datetime
import os
import time
import torch
import argparse
import numpy as np
import sys
sys.path.insert(0, "C:\\Users\\admin\\Desktop\\breeze\\Human-Falling-Detect-Tracks")
from ultralytics import YOLO
import requests
import time
from ctypes.util import find_library
import ctypes as ct
import pyOptris as optris
import datetime
from ultralytics.utils.plotting import Annotator
app = Flask(__name__)

alarm = False
thermal_map = None

def plot_temperature(im, box, temperature, txt_color=(255, 255, 255)):
    lw = max(round(sum(im.shape) / 2 * 0.003), 2)
    sf = lw / 3
    tf = max(lw - 1, 1)
    """Add one xyxy box to image with label."""
    label = "Temperature: {}".format(str(int(temperature)))
    if not isinstance(box, list):
        box = box.tolist()

    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    cv2.rectangle(im, p1, p2, color, thickness=lw, lineType=cv2.LINE_AA)
    w, h = cv2.getTextSize(label, 0, fontScale=sf, thickness=tf)[0]  # text width, height
    outside = p1[1] - h >= 3
    p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
    cv2.rectangle(im, p1, p2, color, -1, cv2.LINE_AA)  # filled
    cv2.putText(im,
                label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                0,
                sf,
                txt_color,
                thickness=tf,
                lineType=cv2.LINE_AA)
    return im


def plot_util(image, h, w, box, temperature, except_case=False):
    fs = int((h + w) * 0.01)  # font size
    annotator = Annotator(image, line_width=round(fs / 6), font_size=fs*10, pil=False)
    if temperature > 100 and not except_case:
        color = (255, 10, 10)
        global alarm
        alarm = True
        send_signal()
    else:
        color = (10, 255, 10)
    annotator.box_label(box, "Temperature: " + str(int(temperature)), color=color, temperature=True)
    return annotator.im
    

def send_signal():
    response = requests.get('http://127.0.0.1:5000/alarm')  # Replace with your Flask app's URL
    if response.status_code == 200:
        print('Signal sent successfully')
    else:
        print('Failed to send signal')


def kpt2bbox(kpt, ex=20):
    """Get bbox that hold on all of the keypoints (x,y)
    kpt: array of shape `(N, 2)`,
    ex: (int) expand bounding box,
    """
    return np.array((kpt[:, 0].min() - ex, kpt[:, 1].min() - ex,
                     kpt[:, 0].max() + ex, kpt[:, 1].max() + ex))


def init_model():
    par = argparse.ArgumentParser(description='Human Fall Detection Demo.')
    par.add_argument('-C', '--camera', default='2',  # required=True,  # default=2,
                     help='Source of camera or video file path.')
    par.add_argument('--model', default='yolov8')
    args = par.parse_args()
    DLL_path = "../irDirectSDK/sdk/x64/libirimager.dll"
    optris.load_DLL()

    # USB connection initialisation 
    optris.usb_init("config_file.xml")

    result = optris.set_palette(optris.ColouringPalette.IRON)

    w, h = optris.get_palette_image_size()
    print("{} x {}".format(w, h))

    fps_time = 0
    f = 0
    alarm_time = time.time()
    model = YOLO('./best.pt')
    while True:
        f += 1
        frame = optris.get_palette_image(w, h)
        result = model.predict(frame, save=False, show_conf=True)
        for res in result:
            res_img = res.plot()
            frame = res_img[..., ::-1]
            print(frame.shape, 'shape', type(frame))
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB if needed
        frame = cv2.UMat(frame)  # Convert numpy array to cv2.Mat object
        frame = cv2.putText(frame, '%d, FPS: %.2f' % (f, 1.0 / (time.time() - fps_time)),
                            (w-150, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        fps_time = time.time()
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Clear resource.
    cv2.destroyAllWindows()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(init_model(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/alarm')
def update_image():
    # Your Python code logic here
    # Check the condition and send the signal when reached
    global alarm
    if alarm:
        # Perform any necessary operations
        # ...
        return jsonify(success=True)
    else:
        return jsonify(success=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
