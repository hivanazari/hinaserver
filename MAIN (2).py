from EasyROI import EasyROI

import cv2
from pprint import pprint
from ultralytics import YOLO
from PIL import Image
import cv2
from shapely.geometry import Polygon
from shapely.geometry import box as bbox
import numpy
import pandas as pd
import json


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

        print(percentage)
    return perst


# load a pretrained model (recommended for training)
model = YOLO("yolov8n.pt")
colorobj = (0, 255, 0)
colorroi = (255, 0, 0)
if __name__ == '__main__':
    video_path = "a.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter('output.avi', fourcc,  20.0, (1280, 720))

    # Initialize cam
    cap = cv2.VideoCapture("b1.mp4")
    ret, frame = cap.read()
    roi_helper = EasyROI(verbose=True)
    # cap.isOpened(), 'Cannot capture source'
    polygon_roi = roi_helper.draw_polygon(frame, 1)
    print("Polygon Example:")
    pprint(type(polygon_roi['roi']))
    for u in polygon_roi['roi']:
        print(u)
    f = open("pes.json", 'w')
    # f.write(polygon_roi['roi'])
    print(polygon_roi['roi'], file=f)
    f.close()

    while True:

        ret, frame = cap.read()

        # # DRAW RECTANGULAR ROI
        # rect_roi = roi_helper.draw_rectangle(frame, 3)
        # print("Rectangle Example:")
        # pprint(rect_roi)

        # frame_temp = roi_helper.visualize_roi(frame, rect_roi)
        # cv2.imshow("frame", frame)
        # cv2.waitKey(1)
        # if key & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()

        # # DRAW LINE ROI
        # line_roi = roi_helper.draw_line(frame, 3)
        # print("Line Example:")
        # pprint(line_roi)

        # frame_temp = roi_helper.visualize_roi(frame, line_roi)
        # cv2.imshow("frame", frame_temp)
        # key = cv2.waitKey(0)
        # if key & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()

        # # DRAW CIRCLE ROI
        # circle_roi = roi_helper.draw_circle(frame, 3)
        # print("Circle Example:")
        # pprint(circle_roi)

        # frame_temp = roi_helper.visualize_roi(frame, circle_roi)
        # cv2.imshow("frame", frame_temp)
        # key = cv2.waitKey(0)
        # if key & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()

        # DRAW POLYGON ROI
        results = model.predict(frame)
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
                            v = {k: v for (k, v) in insect.items() if v > 40}

                            if len(v) > 0:
                                colorobj = (0, 0, 255)
                                k = list(v.keys())
                                keys.extend(k)
                                print(keys)
                                cv2.rectangle(frame, (int(tx[0]), int(
                                    tx[1])), (int(tx[2]), int(tx[3])), colorobj, 2)
                                data = {
                                    "category": "person",
                                    "area": k,
                                    "xyxy": tx
                                    # "date": str(datetime.date.today()),
                                    # "time": str(datetime.time()),
                                }

                            else:
                                colorobj = (0, 255, 0)

                                cv2.rectangle(frame, (int(tx[0]), int(
                                    tx[1])), (int(tx[2]), int(tx[3])), colorobj, 2)

                            # print(tx[0])

                # print(box.xyxy )

        frame_temp = roi_helper.visualize_roi(
            frame, polygon_roi, color=colorroi, keys=keys)
        writer.write(frame_temp)
        # pprint(polygon_roi)

        cv2.imshow("frame", frame_temp)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            writer.release()
            cv2.destroyAllWindows()

        # # '''
        # cv2.imshow("frame", frame)
        # key = cv2.waitKey(0)
        # if key & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        # # '''
