from flask import Flask,abort
from flask import request
from models.ZeroShotApp import ZeroShotApp
import string

import json

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

app = Flask('Emotion')
model = ZeroShotApp()
# emotion_candidate_labels = ["Love", "Joy", "Inspiration", "Hope", "Disgust", "Anger", "Sadness", "Fear", "Neutral", "Worried"]
# emotion_candidate_labels = ["Sadness", "Joy", "Love", "Anger", "Fear", "Surprise", "Doubt", "Hope", "Shame", "Neutral"]
emotion_candidate_labels = ["Sadness", "Indifferent", "Joy", "Love", "Anger", "Fear", "Hope", "Tragic"]

sentiment_candidate_labels = ["Positive", "Negative", "Neutral"]
# candidate_labels = "Joy"

@app.route("/",methods=['POST'])
def emotion():
    if request.method == "POST":
        target_text = request.json["text"]  

        if type(target_text) != str:
            logger.error("(target_text -> %s) , Error 400:Bad Input",target_text)
            return "Error 400: Bad Input",400    
        elif type(emotion_candidate_labels) != list and type(sentiment_candidate_labels) != list:
            logger.error("(emotion_candidate_labels -> {} , Error 400:Bad Input)".format(emotion_candidate_labels))
            logger.error("(sentiment_candidate_labels -> {} , Error 400:Bad Input)".format(sentiment_candidate_labels))
            return "Error 400: Bad Input",400   
        else:
            
            res = sum([i.strip(string.punctuation).isalpha() for i in target_text.split()])
            if res > 5:
                return model.predict(target_text, emotion_candidate_labels, sentiment_candidate_labels)
            
            else:
                
                emotions = {"emotions": [{'predictions': ["Insufficient Info"],'confidence': ["0.0"]}]}
                sentiments = {"sentiments":[{'predictions': ["Insufficient Info"],'confidence': ["0.0"]}]}
                data = [emotions,sentiments]
                
                return json.dumps(data)
    else:
        logger.error("Error 405: Method Not Allowed")
        return "Error 405: Method Not Allowed", 405
        


if __name__ == "__main__":
    app.run(debug=True)

