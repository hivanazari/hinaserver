import threading
import time
import datetime
import cv2
from EasyROI import EasyROI
import json
import cv2
from pprint import pprint
from ultralytics import YOLO
from PIL import Image
import cv2
from shapely.geometry import Polygon
from shapely.geometry import box as bbox
import numpy
from EasyROI import EasyROI
import requests
import base64
roi_helper = EasyROI(verbose=True)
url = 'http://127.0.0.1:8000/detect'
import asyncio

def intersect(poly, rect):
    perst = dict()
    for index, roi in poly['roi'].items():
        poly_vertices = roi['vertices']

    # Create a polygon
        polygon = Polygon(poly_vertices)

        # Create a rectangle
        rectangle = bbox(rect[0], rect[1], rect[2], rect[3])

        # Get the intersection
        intersection = polygon.intersection(rectangle)

        # Print the intersection area
        percentage = intersection.area / rectangle.area * 100
        perst[index] = percentage

        # print(percentage)
    return perst


# load a pretrained model (recommended for training)
model = YOLO("yolov8n.pt")
colorobj = (0, 255, 0)
colorroi = (255, 0, 0)
polygon_roi = dict()
with open('pes.json') as f:
    data = json.loads(f.read().replace("\'", "\""))
print(type(data))
for item in data:
    vl = [x for x in data[item]['vertices'][1:-1].split(' ,  ')]
    fl = []
    for xl in vl:
        fl.extend(eval(xl))
    data[item]['vertices'] = fl
polygon_roi['roi'] = data

polygon_roi['type'] = 'polygon'


class Camera:
    def __init__(self):
        self.thread = None
        self.current_frame = None
        self.last_access = None
        self.res = None
        self.is_running: bool = False
        self.camera = cv2.VideoCapture("b1.mp4")
        if not self.camera.isOpened():
            raise Exception("Could not open video device")
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # load a pretrained model (recommended for training)
        # self.model = YOLO("yolov8n.pt")

    def __del__(self):
        self.camera.release()
   
    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._capture)
            self.thread.start()

    def get_frame(self):
        self.last_access = time.time()

        return self.current_frame, self.res

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.thread = None
    
    def _capture(self):
        self.is_running = True
        self.last_access = time.time()
        time.sleep(1)
        counter=0
        while self.is_running:


            ret, frame = self.camera.read()
            if frame is not None:

                results = model.predict(frame)
                keys = []
                mdata = dict()
                # results = results.numpy()
                # img2 = YOLO..visualize(frame, results)
                # cv2.imshow(img2)
                # cv2.waitKey(1)
                for result in results:
                    colorroi = (255, 0, 0)
                    boxes = result.boxes
                    if len(boxes) > 0:

                        for box in boxes:
                            keys = []
                            if box.cls[0] == float(0):
                                for bxy in box.xyxy:

                                    tx = numpy.array(bxy)
                                    insect = intersect(
                                        polygon_roi, [int(tx[0]), int(tx[1]), int(tx[2]), int(tx[3])])
                                    v = {
                                        k: v for (k, v) in insect.items() if v > 40}

                                    if len(v) > 0:
                                        colorobj = (0, 0, 255)
                                        k = list(v.keys())
                                        keys.extend(k)
                                        # print(keys)
                                        cv2.rectangle(frame, (int(tx[0]), int(
                                            tx[1])), (int(tx[2]), int(tx[3])), colorobj, 2)
                                    
                                        _, encoded_img = cv2.imencode('.png', frame)  # Works for '.jpg' as well
                                        base64_img = base64.b64encode(encoded_img).decode("utf-8")
                                        mdata = {
                                            "category": "person",
                                            "area": str(int(k[0])),
                                            "warning": 1,
                                            "xyxy": str(tx).replace("       ",","),
                                            "date_read": datetime.datetime.today().strftime('%Y-%m-%d'),
                                            "time_read": str(datetime.datetime.now().strftime('%H:%M:%S')),
                                            "main_image":base64_img,
                                        }
                                        headers = {"Accept": "application/json",
                                                "Content-Type": "application/json; charset=utf8"}
                                        data = json.dumps(mdata)
                                        try:
                                            if counter%100==0:
                                                # call get service with headers and params
                                                response = requests.post(
                                                    url, data=data, headers=headers)
                                                print(response)
                                                counter=counter+1
                                        except Exception as ex:
                                            print(ex)

                                    else:
                                        colorobj = (0, 255, 0)

                                        cv2.rectangle(frame, (int(tx[0]), int(
                                            tx[1])), (int(tx[2]), int(tx[3])), colorobj, 2)

                                    # print(tx[0])

                        # print(box.xyxy )

                    frame = roi_helper.visualize_roi(
                        frame, polygon_roi, color=colorroi, keys=keys)
                    self.res = mdata
                if ret:
                    ret, encoded = cv2.imencode(".jpg", frame)
                    if ret:
                        self.current_frame = encoded
                    else:
                        print("Failed to encode frame")
                else:
                    print("Failed to capture frame")
        print("Reading thread stopped")
        self.thread = None
        self.is_running = False
