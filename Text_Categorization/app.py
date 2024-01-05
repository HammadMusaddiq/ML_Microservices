from flask import Flask,abort
from flask import request
from models.ZeroShotApp import ZeroShotApp

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

app = Flask('Categorization')


def create_app(arg1):
    model = ZeroShotApp(arg1)


    @app.route("/",methods=['POST'])
    def cat():
        try:
            if request.method == "POST":    
                target_text = request.json["text"]
                platform = request.json["platform"] 
                # print(target_text, platform)

                if type(target_text) != str:
                    logger.error("(target_text -> %s) , Error 400:Bad Input",target_text)
                    return "Error 400: Bad Input",400

                elif type(platform) != str:
                    logger.error("(target_text -> %s) , Error 400:Bad Input",platform)
                    return "Error 400: Bad Input",400
             
                else:
                    output = model.predict(target_text,platform)
                    logger.info("Model Output Successful")
                    return output

        except Exception as E:
            logger.error(E)
            return E
    
    return app

