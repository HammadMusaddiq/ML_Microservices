from flask import Flask
from flask import request
from models.Detectron2App import Detectron2App

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

app = Flask('OBJD')
model = Detectron2App()

@app.route("/",methods=['POST'])
def objd():

    if request.method == "POST":
        image_url = request.json["imageUrl"]
        if type(image_url)!= str:
            logger.error("Error 400: Bad Input")
            return "Error 400: Bad Input", 400
        else:
            return model.predict(image_url)
    else:
        logger.error("Error 405: Method Not Allowed")
        return "Error 405: Method Not Allowed", 405

@app.route("/get_config",methods=['GET'])
def getConfig():

    if request.method == "GET":
        return {"config":model.getConf()}
    else:
        logger.error("Error 405: Method Not Allowed")
        return "Error 405: Method Not Allowed", 405
if __name__ == "__main__":
    app.run(debug=True)