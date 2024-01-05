import io
import configparser
from ftplib import FTP
from pywebhdfs.webhdfs import PyWebHdfsClient # pip install pywebhdfs
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


class FtpApp():

    def __init__(self):
        # Parsing Local Config File ../config.ini to get ip & port
        self.parse_str = configparser.ConfigParser()
        self.parse_str.read("../config.ini")
        
        self.node_ip_ftp = None
        self.node_port_ftp = None
        self.auth_user_ftp  = None
        self.auth_pass_ftp  = None
        self.node_ip_MDS_Video = None
        self.node_port_MDS_Video = None
        self.kafka_broker = None
                
        self.node_ip_ftp = str(self.parse_str.get('FTP', 'host')).strip()
        self.node_path_ftp = str(self.parse_str.get('FTP', 'path')).strip()
        self.node_port_ftp = int(self.parse_str.get('FTP', 'port'))
        self.auth_user_ftp = str(self.parse_str.get('FTP', 'username')).strip()
        self.auth_pass_ftp = str(self.parse_str.get('FTP', 'password')).strip()

        self.node_ip_MDS_Video = str(self.parse_str.get('MDS_VIDEO', 'ip')).strip()
        self.node_port_MDS_Video = int(self.parse_str.get('MDS_VIDEO', 'port'))
        self.kafka_broker = str(self.parse_str.get('KAFKA_BROKERS', 'brokers')).strip()
        print(self.node_port_ftp,self.node_ip_ftp)

        # self.ftp = FTP(host=self.node_ip_ftp,user=self.auth_user_ftp,passwd=self.auth_pass_ftp)
        self.ftp = FTP()
        self.ftp.connect(host=self.node_ip_ftp, port=self.node_port_ftp)
        self.ftp.login(user=self.auth_user_ftp, passwd=self.auth_pass_ftp)

        self.change_to_video_download_dir()

    def change_to_video_download_dir(self):
        video_download_path = '/MDS_Downloads/MDS_Video'
        try:
            if self.ftp.pwd() != video_download_path:
                self.ftp.cwd(video_download_path) #if error on changing cwd then make in exception
                logger.info("Changed current ftp directory to {}".format(video_download_path))
        except:
            try:
                for folder in video_download_path.split('/')[1:]:
                    self.chdir(folder)
                logger.info("Changed current ftp directory to {}".format(video_download_path))

            except Exception as E:
                logger.error("An Exception occured in while changing directory in FTP : {}".format(E)) 
                

    def getFTP(self):
        return self.ftp

    def retry_ftp_connection(self):
        is_connected = False
        # 5 retries
        for i in range(5):
            if self.connect() == True:
                #print('connected')
                logger.info("connection established with FTP")
                if self.login() == True:
                    self.change_to_video_download_dir()
                    logger.info("Login with FTP successful")
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
            self.ftp.retrlines('LIST')
        except:
            return False
        return True
        

    def connect(self):
        try:
            logger.info("Trying FTP Connection ({},{},{},{})".format(self.node_ip_ftp,self.node_port_ftp,type(self.node_ip_ftp),type(self.node_port_ftp)))
            self.ftp.connect(host=self.node_ip_ftp, port=self.node_port_ftp)
            return True
        except Exception as E:
            logger.error("FTP Connect Error {}".format(E))
            return E

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
        print(self.ftp.pwd())
        if self.directory_exists(dir) is False:
            self.ftp.mkd(dir)
        self.ftp.cwd(dir)

# for testing
# ftp_connection = FtpApp()
# print(ftp_connection.node_ip_ftp)
# print(type(ftp_connection.node_port_ftp))
# print(ftp_connection.connect())
