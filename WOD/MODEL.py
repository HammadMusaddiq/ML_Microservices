from pathlib import Path
import json
import torch
import torch.backends.cudnn as cudnn
import numpy as np
from PIL import Image
import cv2
import io, requests
import os
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, set_logging
from utils.torch_utils import select_device, load_classifier, TracedModel

import logging
logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s | %(message)s')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

class Model:
    agnostic_nms = False
    augment=False
    classes = None
    conf_thres=0.6
    device = 'cpu' #0, 1, 2, 3 for gpu ------ for cpu empty string or 'cpu'
    exist_ok = False
    img_size = 640
    iou_thres = 0.45
    name = 'exp'
    no_trace = False
    nosave = False
    project = 'runs/detect'
    save_conf=False
    save_txt=False
    update=False
    view_img=False
    weights=['best.pt']
    model=''
    stride = ''
    imgsz = ''
    half = ''

    def __init__(self, agnostic_nms = False,
    augment=False,
    classes = None,
    conf_thres=0.6,
    device = '', #0, 1, 2, 3 for gpu ------ for cpu empty string or 'cpu'
    exist_ok = False,
    img_size = 640,
    iou_thres = 0.45,
    name = 'exp',
    no_trace = False,
    nosave = False,
    project = 'runs/detect',
    save_conf=False,
    save_txt=False,
    # source='1.jpg'
    update=False,
    view_img=False,
    weights=['best.pt']):
        weights, view_img, save_txt, self.imgsz, trace = weights, view_img, save_txt, img_size, not no_trace
        # Initialize
        set_logging()
        self.device = select_device(device)
        self.half = self.device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        self.model = attempt_load(weights, map_location=self.device)  # load FP32 model
        logger.info("Model Loaded in Memory")
        self.stride = int(self.model.stride.max())  # model stride
        self.imgsz = check_img_size(self.imgsz, s=self.stride)  # check img_size

        if trace:
            self.model = TracedModel(self.model, self.device, img_size)
            logger.info("Traced Model Loaded in Memory")
        if self.half:
            self.model.half()  # to FP16
            logger.info("Device Model Loaded in Memory")

    def letterbox(self, img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
        # Resize and pad image while meeting stride-multiple constraints
        img = cv2.resize(img, (640,640), cv2.INTER_AREA)
        shape = img.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:  # only scale down, do not scale up (for better test mAP)
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
        if auto:  # minimum rectangle
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
        elif scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
        return img, ratio, (dw, dh)

    def convert_2d_to_3d(self, image):
        image.save('current.png')
        img = cv2.imread('current.png')
        os.remove('current.png')
        return img

    def transform(self, image_bytes):
        img = Image.open(image_bytes)
        arr = np.float32(img)
        image_shape = arr.shape
        if len(image_shape)<3:
            img = self.convert_2d_to_3d(img)
            arr = np.float32(img)
            image_shape = arr.shape

        # if image_shape[2] != 3: # convering image to 3 channels for extracting embeddings
        #     arr = arr[:,:,:3]
        return arr

    
    def detect(self, source):
        # Second-stage classifier
        classify = False
        if classify:
            modelc = load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=self.device)['model']).to(self.device).eval()

        dataset=[source]

        # Get names and colors
        names = self.model.module.names if hasattr(self.model, 'module') else self.model.names

        # Run inference
        if self.device.type != 'cpu':
            self.model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(self.device).type_as(next(self.model.parameters())))  # run once
        
        old_img_w = old_img_h = self.imgsz
        old_img_b = 1

        for img in dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            
            if img.ndimension() == 3:
                img = img.unsqueeze(0)
            # img = img.permute(0, 3, 1, 2)
            # Warmup
            if self.device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    self.model(img, augment=self.augment)[0]

            # Inference
            pred = self.model(img, augment=self.augment)[0]

            # Apply NMS
            pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=self.classes, agnostic=self.agnostic_nms)
        return pred
