#Import Flask
from flask import json

#Import Libraries for your model
from transformers import pipeline

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

class ZeroShotApp:

    def __init__(self):
        self.classifier = pipeline("zero-shot-classification",model="vicgalle/xlm-roberta-large-xnli-anli", device = 0)

    def get_model(self):
        return self.classifier

    def predict(self, x,y,z):
        target_text = x
        emotion_candidate_labels = y
        sentiment_candidate_labels = z
        
        try:
            emotion_result = self.classifier(target_text, emotion_candidate_labels)
            emotion_label = emotion_result["labels"][0]
            emotion_score = emotion_result["scores"][0]
            
            if emotion_score < 0.25:
                emotion_label = "Indifferent"
#                 emotion_score = 0.0
            
            emotions = {"emotions": [{'predictions': [str(emotion_label)],'confidence': [str(emotion_score)]}]}  


            sentiment_result = self.classifier(target_text, sentiment_candidate_labels)
            sentiment_label = sentiment_result["labels"][0]
            sentiment_score = sentiment_result["scores"][0]
            
            sentiments = {"sentiments":[{'predictions': [str(sentiment_label)],'confidence': [str(sentiment_score)]}]}

            data = [emotions,sentiments]

            return json.dumps(data)
        except Exception as E:
            logger.error("Error 500:Internal Server Error")
            return str(E), 500
        

