# from pathlib import Path
import json
# import torch
# import torch.backends.cudnn as cudnn
import numpy as np
from PIL import Image
from flask import Flask, request
import cv2
import io, requests
# import os
# from models.experimental import attempt_load
# from utils.general import check_img_size, non_max_suppression, set_logging
# from utils.torch_utils import select_device, load_classifier, TracedModel
from MODEL import Model


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

logger.info("App started")

weapon_model = Model()





app = Flask(__name__)



class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/insert', methods=['POST'])
def main():
    try:
        try:
            image = request.files['image_path']
            frame = weapon_model.transform(image)
        except:
            try:
                nparr = np.fromstring(request.data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except:
                # print('Second Except')
                link =request.form['image_path']
                response = requests.get(link)
                img = Image.open(io.BytesIO(response.content))
                arr = np.uint8(img)
                frame = arr


        img0 = frame  # BGR
        # print(img0.shape)
        # cv2.imshow('', img)
        # cv2.waitKey(0)
        
        # Padded resize
        img = weapon_model.letterbox(img0, weapon_model.img_size, stride=weapon_model.stride)[0]
        
        # cv2.imshow('', img)
        # cv2.waitKey(0)
        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        source = img #np.expand_dims(frame, 0)
        
        
        
        pred = weapon_model.detect(source)


        labels = ['Grenade', 'Gun', 'Knife', 'Pistol']
        predictions = pred[0]
        con = []
        bbox = []
        label = []
        if len(predictions) > 0:
            for each in predictions:
                con.append(float(each[4])*100)
                bbox.append(each[:4].cpu().detach().numpy())
                label.append(labels[int(each[5])])

        data = {'confidence':con,
                'bbox':bbox,
                'label':label}

        print(data)
        logger.info("Model Output Successful")
        return json.dumps(data, cls=NumpyEncoder)
    except Exception as E:
        logger.error(E)
        return E



if __name__ == '__main__':

    app.run(debug=True, host = '0.0.0.0', port=5017)

