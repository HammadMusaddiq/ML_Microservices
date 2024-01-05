import numpy as np
from ftplib import FTP, error_perm
import requests
import io
from PIL import Image
import requests
import datetime
import configparser

import logging
import random
import uuid


logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()

formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s | %(message)s')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


class MDSImageApp:
    
    def __init__(self):
        # Parsing Local Config File ../config.ini to get ip & port
        self.parse_str = configparser.ConfigParser()
        self.parse_str.read("../config.ini")
        
        self.node_ip_ftp = None
        self.node_path_ftp = None
        self.node_port_ftp = None
        self.auth_user_ftp  = None
        self.auth_pass_ftp  = None

        self.node_ip_ftp = str(self.parse_str.get('FTP', 'host')).strip()
        self.node_path_ftp = str(self.parse_str.get('FTP', 'path')).strip()
        self.node_port_ftp = int(self.parse_str.get('FTP', 'port'))
        self.auth_user_ftp = str(self.parse_str.get('FTP', 'username')).strip()
        self.auth_pass_ftp = str(self.parse_str.get('FTP', 'password')).strip()
        
        # self.ftp = FTP(host=self.node_ip_ftp,user=self.auth_user_ftp,passwd=self.auth_pass_ftp)
        self.ftp = FTP()
        self.ftp.connect(host=self.node_ip_ftp, port=self.node_port_ftp)
        self.ftp.login(user=self.auth_user_ftp, passwd=self.auth_pass_ftp)

        self.base_url = "http://"+self.node_ip_ftp+self.node_path_ftp
        self.dir_path = "/MDS_Downloads/MDS_Image"
        self.change_ftp_present_working_dir(self.dir_path)

    def change_ftp_present_working_dir(self, pwd_path):
        try:
            if self.ftp.pwd() != pwd_path:
                self.ftp.cwd(pwd_path) 
                logger.info("Changed current ftp directory to {}".format(self.ftp.pwd()))
        except:
            try:
                for folder in pwd_path.split('/')[1:]:
                    self.chdir(folder)
                logger.info("Changed current ftp directory to {}".format(self.ftp.pwd()))
            except Exception as E:
                logger.error("An Exception occured in while changing directory in FTP : {}".format(E)) 


    def getFTP(self):
        return self.ftp

    def getBaseURL(self):
        return self.base_url

    def retry_ftp_connection(self):
        is_connected = False
        # 5 retries
        for i in range(5):
            if self.connect() == True:
                #print('connected')
                # logger.info("connection established with FTP")
                if self.login() == True:
                    # self.change_to_video_download_dir()
                    # logger.info("Login with FTP successful")
                    is_connected = True
                    return is_connected
            else:
                # FTP connection Error
                error = "FTP Connection Error"
                E = self.ftp.connect()
                logger.error("{} Reason: {}".format(error,E))
                # return is_connected

    def is_connected(self):
        try:
            self.ftp.pwd()
            return True
        except:
            return False

    def connect(self):
        try:
            # logger.info("Trying FTP Connection ({},{},{},{})".format(self.node_ip_ftp,self.node_port_ftp,type(self.node_ip_ftp),type(self.node_port_ftp)))
            self.ftp.connect(host=self.node_ip_ftp, port=self.node_port_ftp)
            return True
        except Exception as E:
            logger.error("FTP Connect Error {}".format(E))
            return E

    def retry_connect(self):
        for i in range(5):
            if self.ftp.connect(self.node_ip_ftp, self.node_port_ftp):
                break   
        return True

    def login(self):
        try:
            self.connect()
            self.ftp.login(self.auth_user_ftp, self.auth_pass_ftp)
            return True
        except Exception as E:
            return E

    def directory_exists(self, dir):
        filelist = []
        self.ftp.retrlines('LIST', filelist.append)
        #print(filelist)
        for f in filelist:
            if f.split()[-1] == dir and f.upper().startswith('D'):
                return True
        return False

    def chdir(self, dir):
        # print(self.ftp.pwd())
        if self.directory_exists(dir) is False:
            self.ftp.mkd(dir)
        self.ftp.cwd(dir)


    def transformImage(self, url):
        try:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            arr = np.uint8(img)
            return arr

        except Exception:
            return False

    def imageToFTP(self, image_link):
        
        if not self.is_connected():
            self.retry_ftp_connection()
            self.change_ftp_present_working_dir(self.dir_path)
        # else:
        #     self.change_ftp_present_working_dir(self.dir_path)
        
        image = self.transformImage(image_link)

        if image is not False:
            print(f"Input Image link: {image_link}")
            
            PIL_image = Image.fromarray(np.uint8(image)).convert('RGB')
            temp = io.BytesIO() # This is a file object
            PIL_image.save(temp, format="jpeg") # Save the content to temp
            # temp1 = temp.getvalue() # To print bytes string
            temp.seek(0) # Return the BytesIO's file pointer to the beginning of the file

            
            # ran_number = random.getrandbits(25)

            # time = datetime.datetime.now().today()
            # date_time = time.strftime("%d%m%Y_%H%M%S")
            # img_name = "Img" + str(date_time) + "_" + str(ran_number) +".jpeg"

            img_name = (str(uuid.uuid4())) + ".jpeg"

            # Store image to FTP Server
            print(self.ftp.storbinary("STOR " + img_name, temp))

            FTP_URL = f"{self.base_url + self.dir_path}"
            FTP_Img =  FTP_URL + "/" + img_name

            print("File saved to FTP SUCCESSFULLY: ", FTP_Img)

            return {"url" :FTP_Img}

        else:
            message = f"Error! 404 Url does not exist: {image_link}"
            logger.error(message)
            print(message)
            return {"url": image_link}
        
      
       
  


   