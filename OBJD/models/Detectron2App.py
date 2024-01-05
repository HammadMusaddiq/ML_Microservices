from detectron2.engine import DefaultPredictor
from detectron2.data import MetadataCatalog
from detectron2.config import get_cfg
from detectron2 import model_zoo
import cv2 
from skimage import io

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

class Detectron2App:

    def __init__(self):
        # Configuration of model
        self.cfg = get_cfg()
        self.model_file = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"
        self.cfg.merge_from_file(model_zoo.get_config_file(self.model_file))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(self.model_file)
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.9
        self.cfg.MODEL.DEVICE='cpu'
        self.class_names = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]).thing_classes
        self.model = DefaultPredictor(self.cfg)

    def transformImage(self, url):
        img = io.imread(url)
        img_cvt = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img_cvt

    def getConf(self):
        return self.cfg

    def getClassNames(self):
        return self.class_names
    
    def getModel(self):
        return self.model

    def getPredAxis(self,prediction_output):
        # Axis of Predicted Objects in Images
        pred_axis = prediction_output['instances'].pred_boxes.tensor.tolist()
        pred_axis_round = []
        for axis in pred_axis:
            pred_axis_round.append(['%.5f' % val for val in axis])
        return pred_axis_round

    def getPredClass(self,prediction_output):
        # Predicted classes 
        p_classes = prediction_output['instances'].pred_classes.tolist()
        p_class_names = list(map(lambda classes: self.class_names[classes], p_classes))
        return p_class_names

    def getProbScore(self,prediction_output):
        # Probability Scores
        p_scores = prediction_output['instances'].scores.tolist()
        p_scores_round = ['%.2f' % val for val in p_scores]
        return p_scores_round

    def predict(self, image_url):
        results = []
        if image_url:
            try:
                # Make Prediction
                prediction_output = self.model(self.transformImage(image_url))
                try:
                    # Pred Axis
                    pred_axis_round = self.getPredAxis(prediction_output)

                    # Pred Class Names
                    p_class_names = self.getPredClass(prediction_output)
                    
                    # Probabiltiy Score
                    p_scores_round = self.getProbScore(prediction_output)
                    results.append({"predicted_axis":pred_axis_round,"object_classified":p_class_names,"probability_score":p_scores_round})
                except Exception as E:
                    error = "Error in transforming Image of URL: {} Reason: {}".format(str(image_url),E) 
                    logger.error(error)

            except Exception as E:
                error = "Error in transforming Image of URL: {} Reason: {}".format(str(image_url),E) 
                logger.error(error)
            return {"data": results}
        else:
            error = "No Image Url in the data."
            logger.error(error)

            return {"data": results}

    