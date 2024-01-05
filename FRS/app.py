from flask import Flask
from flask import request
from models.FacenetApp import FacenetApp
from models.Milvus import Milvus
import operator
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

app = Flask('IMG_EMBEDDINGS')
model = FacenetApp()
milvus = Milvus()

@app.route("/",methods=['GET'])
def hello():
    return "FACENET is Up and Running" , 200

@app.route("/",methods=['POST'])
def img_embeddings():
    # import pdb;pdb.set_trace()
    if request.method == "POST":
        try:
            image_link = request.json["imageUrl"]
        except:
            logger.error("Error 400: Bad Input")
            return "Error 400: Bad Input", 400
        
        logger.info("Inserting started")
        try:
            logger.info("Starting extracting embeddings.")
            embeddings = model.predict(image_link)['data']
        except Exception as E:
            error = "An Exception Occured: {}".format(E)
            logger.error(error)
            return error, 500

        if len(embeddings) == 0: # if no face found or error occured in embeddings extraction
            return {"milvus_id":''}
        
        elif embeddings == 'Image Resolution is Low':
            return {'milvus_id':'Image Resolution is Low'}

        else:
            try:
                milvus_ids = []
                logger.info("Starting inserting embeddings in the Milvus DB.")
                for emb in embeddings:
                    idx = milvus.insert(emb,image_link)
                    if idx:
                        milvus_ids.append(idx)
                
                if milvus_ids:
                    check = milvus.dumpToElasticSearch(milvus_ids,image_link)
                    if check == True:
                        logger.info("Milvus ID has been saved in ES, Process completed with success.")
                        return {"milvus_id":milvus_ids} # milvus ids of all extracted faces embeddings

                else: # returing false, means embeddings not saved on milvus database
                    return False

            except Exception as E:
                error = "An Exception Occured: {}".format(E)
                logger.error(error)
                return error,500
                
    else:
        error = "Error 405: Method Not Allowed"
        logger.error(error)
        return error, 405


@app.route("/milvus/search",methods=['POST'])
def milvus_search():
    if request.method == "POST":
        try:
            image_link = request.json["imageUrl"]
        except:
            logger.error("Error 400: Bad Input")
            return "Error 400: Bad Input", 400

        logger.info("Searching started")
        try:
            logger.info("Starting extracting embeddings.")
            embeddings = model.predict(image_link)['data']
        except Exception as E:
            error = "An Exception Occured: {}".format(E)
            logger.error(error)
            return error, 500

        if len(embeddings) == 0: # if no face found in the image then embedding list will be empty, so return empty matched_images
            return {"matched_images":[]}
        
        elif embeddings == 'Image Resolution is Low': # tacked from front-end
            return {"matched_images":[]}

        else:
            try:
                matched_images = []
                logger.info("Starting searching similar embeddings.")
                for emb in embeddings:
                    image_list = milvus.search(emb)
                    if image_list != False:
                        matched_images.extend(image_list)
                
                #import pdb;pdb.set_trace()
                if matched_images:
                    # Remove duplicates based on a single key in dict
                    K = "url"
                    
                    memo = set()
                    res = []
                    for sub in matched_images:
                        
                        # testing for already present value
                        if sub[K] not in memo:
                            res.append(sub)
                            
                            # adding in memo if new value
                            memo.add(sub[K])

                    logger.info("Matched images has been extracted, process completed with success.")
                    return {"matched_images":sorted(res, key=operator.itemgetter('distance'), reverse=False)} # list of (list of dictionary) if matched otherwise []
                
                elif matched_images == [] and image_list != False: # if no image matched
                    logger.info("No matched image found, process completed with success.")
                    return {"matched_images":[]}

                else: # returing false, means searching failed on milvus database
                    return False

            except Exception as E:
                error = "An Exception Occured: {}".format(E)
                logger.error(error)
                return error,500
    else:
        error = "Method Not Allowed"
        logger.error(error)
        return error,405

if __name__ == "__main__":
    app.run(debug=True)