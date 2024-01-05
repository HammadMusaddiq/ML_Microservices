from flask import Flask
from flask import request
from models.MDSImageApp import MDSImageApp
import requests
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

app = Flask("MDS_Image")
model = MDSImageApp()

@app.route("/", methods=['POST'])
def image_to_FTP():
    if request.method == "POST":
        image_link = request.json["imageUrl"]
        #image_link = request.args.get("imageUrl")
        try:
            logger.info("Process Started")
            logger.info(f"Image: {image_link} downloading to FTP started")
            response = model.imageToFTP(image_link)
        except Exception as E:
            print(E)
            response = {"url":image_link}
        
        logger.info(f"Image: {image_link} stored to FTP successfully on the following link: {response.get('url')}")
        logger.info("Process Finished")
        return response
    else:
        logger.error("Error 405: Method not Allowed")
        return "Error 405: Method not Allowed"


if __name__ == "__main__":
    app.run(debug=True) 

  