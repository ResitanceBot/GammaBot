from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
 
# Load the model.
model = YOLO('yolov8n.pt')

dict_classes = model.model.names

# Training.
results = model.train(
   data='data.yaml',
   imgsz=640,
   epochs=10,
   batch=8,
   name='yolov8n_custom'
)
