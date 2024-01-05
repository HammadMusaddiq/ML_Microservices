from flask import Flask
from flask import request
from models.LabseApp import LabseApp


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

model = LabseApp()
app = Flask("LABSE")

@app.route('/',methods=['POST'])
def getEmbeddings():
    if request.method == "POST":
        try:
            sentences = request.get_json()['text']
        except Exception as E:
            error = "500 Internal Server: Unable to Get text field"
            logger.error(error)
            return error, 500
        try: 
            embeddings = model.predict(sentences)
            return {"data":embeddings}, 200
        except Exception as E:
            error = "500 An Exception Occured:  {}".format(E)
            logger.error(error)
            return error, 500 
    
    else:
        error = "405 Method not Allowed"
        logger.error(error)
        return error, 405

if __name__ == "__main__":
    app.run(debug=True)