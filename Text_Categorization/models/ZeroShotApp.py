#Import Flask
from flask import json

#Import Libraries for your model
from transformers import pipeline
import string

import configparser
from pywebhdfs.webhdfs import PyWebHdfsClient

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


import ast

class ZeroShotApp:

    
    def __init__(self,custom):
        self.custom = custom
        self.classifier = pipeline("zero-shot-classification",model="vicgalle/xlm-roberta-large-xnli-anli", device = 0)
        logger.info("Model Loaded in Memory")
        self.local_config_parses = configparser.ConfigParser()
        self.local_config_parses.read("config.ini")

        #Main Categories
        self.others_cat_in = ast.literal_eval(self.local_config_parses[self.custom]['others_cat_in'])
        self.others_cat_out = ast.literal_eval(self.local_config_parses[self.custom]['others_cat_out'])

        # #Linkedin Categories

        self.linkedin_cat_in = ast.literal_eval(self.local_config_parses[self.custom]['linkedin_cat_in'])
        self.linkedin_cat_out = ast.literal_eval(self.local_config_parses[self.custom]['linkedin_cat_out'])

    
    def get_list(self,main_pred):

        main_cat = ["Arts & Culture","Economy","Entertainment","Fashion","Food and Dining","Education","Science and Technology",\
                                    "Sports","Travel and Adventure","Politics","Health and Medicine","Weather","Religion"]


        cat_list = [["art_cat_in","art_cat_out"],["economy_cat_in","economy_cat_out"],["ent_cat_in","ent_cat_out"],\
                            ["fashion_cat_in","fashion_cat_out"],["food_cat_in",'food_cat_out'],["edu_cat_in","edu_cat_out"],["tech_cat_in","tech_cat_out"],["sports_cat_in","sports_cat_out"],\
                            ["travel_cat_in","travel_cat_out"],['politics_cat_in',"politics_cat_out"],["health_cat_in",'health_cat_out'],["weather_cat_in","weather_cat_out"],\
                            ["religion_cat_in","religion_cat_out"]]
        

        sub_list = []
        a_list =[]
        b_list = []
        
        for val_1,val_2 in zip(main_cat,cat_list):

          if val_1 == main_pred:
              sub_list = val_2

        a_list = ast.literal_eval(self.local_config_parses[self.custom][sub_list[0]])
        b_list = ast.literal_eval(self.local_config_parses[self.custom][sub_list[1]]) 

        return a_list, b_list

        

    def get_model(self):
        return self.classifier

    def get_cat(self,text,thresh,cat_in,cat_out):
        predictions = []
        confidence = []
        for lst_in,lst_out in zip(cat_in,cat_out):
          result = self.classifier(text, lst_in)
          label = result["labels"][0]
          score = result["scores"][0]

          if score > thresh:

            for val_1,val_2 in zip(lst_in,lst_out):

                if val_1 == label:
                    if val_2 != "":
                        predictions.append(val_2)
                        confidence.append(score)
          
                    else:
                        predictions.append(val_1)
                        confidence.append(score)

        if not predictions:
          predictions.append("Other")
          confidence.append("0.0")

        return predictions,confidence 

    def predict(self, x, y):
        target_text = str(x)
        platform = str(y)
        predictions = []
        confidence = []
        pred = []
        conf = []
        res = sum([i.strip(string.punctuation).isalpha() for i in target_text.split()])
        

        try:
            if res > 5:
        
               
                if platform == 'linkedin':

                    predictions,confidence= self.get_cat(target_text,0.1,self.linkedin_cat_in, self.linkedin_cat_out)

                    if predictions[0] == "Other":
                      pred.append("Other")
                      conf.append("0.0")
                    else:
                      pred.append(predictions[0])
                      conf.append(confidence[0]) 

                    predictions.append(pred[0])
                    confidence.append(conf[0])

                else:
                    
                    predictions,confidence= self.get_cat(target_text,0.1,self.others_cat_in, self.others_cat_out)

                    if predictions[0] == "Other":
                      pred.append("Other")
                      conf.append("0.0")

                    else:

                      in_list, out_list = self.get_list(predictions[0])
                      

                      pred,conf = self.get_cat(target_text,0.1,in_list, out_list)
                      
                    
                    predictions.append(pred[0])
                    confidence.append(conf[0])  

            else:
                predictions.append("Insufficient Info")
                confidence.append("0.0")

            
 
            data = {"confidence": confidence, "predictions": predictions}
            return json.dumps(data)    
        except Exception as E:
            logger.error("Error 500:Internal Server Error")
            print(str(E))
            return str(E), 500



