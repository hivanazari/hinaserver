from ultralytics import YOLO
from PIL import Image
import cv2

# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
# results = model.train(data="coco128.yaml", epochs=3)  # train the model
# results = model.val()  # evaluate model performance on the validation set
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
results = model.predict(source="a.mp4", show=True)
# results = model.predict(source="folder", show=True) # Display preds. Accepts all YOLO predict arguments
