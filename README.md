
##### List of Contents
1. [Getting Started](#markdown-header-getting-started)
2.  [PORT Table](#markdown-header-port-table)
3. [NER](#markdown-header-ner)
4. [Object Detection](#markdown-header-object-detection)
5. [Facial Recognition Service (FRS) (incomplete)](#markdown-header-facial-recognition-service)
6. [LABSE](#markdown-header-labse)
7. [MDS Video](#markdown-header-mds-video)
8. [MDS Image](#markdown-header-mds-image)
9. [Text Categorization](#markdown-header-text-categorization)
10. [EmoSent](#markdown-header-emosent) 
11. [Weapon Object Detection](#markdown-header-weapon-object-detection) 
12. [Updating the Virtual Environments](#markdown-header-updating-the-virtual-environments) 
13.  [Important Notes](#markdown-header-important-notes)
 

# Getting Started
SSH into the remote VM/Droplet/Server

ssh key setup for repository secure access

```bash
ssh-keygen # set up your public/private key
cat ~/.ssh/id_rsa.pub # copy ssh public key
```

Add the copied ssh into your account settings
```
1. From Bitbucket, choose Personal settings from your avatar in the lower left.

2. Click SSH keys. If you've already added keys, you'll see them on this page.

3. From Bitbucket, click Add key.

4. Enter a Label for your new key, for example, Default public key.

5. Paste the copied public key into the SSH Key field.

6. Click Save.
```

Update ubuntu distribution

```bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-pil python-pyrex idle-python2.7 libgle3 -y

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update -y

sudo apt-get install git

git clone -b development git@...git

sudo apt-get install python3.6 
sudo apt-get install python3.6-dev
sudo apt-get install python3.6-distutils

sudo apt-get install ffmpeg
sudo apt-get install docker
sudo apt-get install docker-compose
```

screen is used to open multiple sessions. When the user exits terminal while using ssh, the processes/services will still be running in the background.

```bash
sudo apt-get install screen
```

Supervisor is a process manager which provides a singular interface for managing and monitoring a number of long-running programs. We will be using multiple rq workers.

```bash
sudo apt-get install supervisor
sudo systemctl status supervisor
```

To install the virtualenv package:

```bash
sudo apt-get install virtualenv
```

Clone the repo in ```/opt``` directiry

```bash
git clone -b development git@...git
```

change directory into 

```bash
cd /opt/ml_microservices
```

For the Virtual Environments, create a separate folder in  ```/opt```

```bash
cd /opt
mkdir Virtual_Environments
```

# PORT Table

The list of Microservices and their respective ports are the following:

| SERVICE | PORT |
|:---:|:---:|
| NER | 5001 |
| OBJD | 5002 |
| FRS | 5003 |
| LABSE | 5004 |
| MDS-VIDEO | 5007 |
| MDS-IMAGE | 5008 |
| CATEGORIZATION | 5012 |
| EMOSENT | 5016 |
| WOD | 5017 |



# NER

Named Entity Recognition (NER) using Deeppavlov Multi BERT.  Microservice is used only by the NER stream.
Output is shown on front end in the "Talks About" section in Profile Info.

## Virtual Environment Creation 
Change directory into 
```bash
cd /opt/Virtual_Environments
```
Create the Environment for NER:

```bash
virtualenv --python=/usr/bin/python3.6 ner_env
```
Activate the virtual environment:

```bash
source ner_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/NER/requirements.txt"
```

## Starting the microservice

Create a seperate screen for NER

```bash
screen -S NER
```
Activate the virtual environment:
```bash
source /opt/Virtual_Environments/ner_env/bin/activate
```
Change directory into 
```bash
cd /opt/ml_microservices/NER
```
Run Service

```bash
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5001 app:app 
```

Detach Screen 

```bash
CTR + A, D 
```

## Usage

```python
import requests

#send post request on ip and port for NER from config
response = requests.post(ip:port, json={"text": list_of_strings})

print(response.json()["data"])
```

# Object Detection

Object Detection with Detectron2

## Virtual Environment Creation 

Change directory into 
```bash
cd /opt/Virtual_Environments
```

Create the Environment for OBJD:

```bash
virtualenv --python=/usr/bin/python3.6 objd_env
```
Activate the virtual environment:

```bash
source objd_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/OBJD/requirements.txt"
```

Install Torch, TorchVision and TorchAudio (CPU):

```bash
pip install torch==1.10.1+cpu torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
```

Install detectron2:

```bash
python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html
```

## Starting the microservice

Create a seperate screen for OBJD

```bash
screen -S OBJD
```
Activate the virtual environment:
```bash
source /opt/Virtual_Environments/objd_env/bin/activate
```
Change directory into 
```bash
cd /opt/ml_microservices/OBJD
```
Run Service

```bash
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5002 app:app 
```

Detach Screen 

```bash
CTR + A, D 
```

## Usage

```python
import requests

#send post request on ip and port for OBJD from config
response = requests.post(ip:port, json={"imageUrl": image_url_in_string})

print(response.json()["data"])
```

# Facial Recognition Service 

Image Embeddings for Facial Recognition (FRS) using Facenet. The microservice gets embeddings of the image and saves it in milvus database.

## Virtual Environment Creation 

Change directory into 
```bash
cd /opt/Virtual_Environments
```

Create the Environment for FRS:

```bash
virtualenv --python=/usr/bin/python3.6 frs_env
```
Activate the virtual environment:

```bash
source frs_env/bin/activate
```

Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/FRS/requirements.txt"
```

Install CMake:

```bash
pip install -r "../ml_microservices/FRS/requirements.txt"
```

Install Torch, TorchVision, and TorchAudio packages (CPU):

```bash
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
```

Install Torch, TorchVision, and TorchAudio packages (GPU):

```bash
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
```

## Starting the microservice

Create a seperate screen for FRS:

```bash
screen -S FRS
```

Activate the virtual environment:
```bash
source /opt/Virtual_Environments/frs_env/bin/activate
```

Change directory into 
```bash
cd /opt/ml_microservices/FRS
```

Run Service (Better to use "flask run" command for FRS):

```bash
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5003
or 
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5003 app:app 
```

Detach Screen 

```bash
CTR + A, D 
```

## To Run Mivlus Docker Image

```bash
sudo docker-compose up -d
```

Check the status of the container:

```bash
sudo docker-compose ps
```

To restart docker milvus container:

```bash
sudo docker restart milvus-standalone milvus-minio milvus-etcd
```

## Usage

```python
import requests

# To Extract Image Embeddings and save it on the Milvus Database
response = requests.post(ip:port, json={"imageUrl": single_image_url_string})
print(response.json()["data"])

# To Search for Similar Images, we are using Milvus Search
response = requests.post(ip:port+"/milvus/search", json={"imageUrl": single_image_url_string})
print(response.json()["data"])

```

# LABSE

LABSE is a multilingual embedding model that is a powerful tool which encodes text from different languages into a shared embedding space, enabling it to be applied to a range of downstream tasks, like text classification, clustering, and others, while also leveraging semantic information for language understanding. This microservice is currently being used for Emotion and Sentiment Analysis.

## Virtual Environment Creation 

Change directory into 
```bash
cd /opt/Virtual_Environments
```

Create the Environment for LABSE:

```bash
virtualenv --python=/usr/bin/python3.6 labse_env
```
Activate the virtual environment:

```bash
source labse_env/bin/activate
```

Install CMake:

```bash
pip install cmake==3.18.4.post1
```

Install **Sentence Transformer** packages:

```bash
pip install sentence_transformers
```

Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/LABSE/requirements.txt"
```

## Starting the microservice

Create a seperate screen for LABSE

```bash
screen -S LABSE
```

Activate the virtual environment:
```bash
source /opt/Virtual_Environments/labse_env/bin/activate
```
Change directory into 
```bash
cd /opt/ml_microservices/LABSE
```

Run Service

```bash
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5004 app:app 
```

Detach Screen 

```bash
CTR + A, D 
```

## Usage

```python
import requests

#send post request on ip and port for LABSE from config
response = requests.post(ip:port, json={"text": list_of_strings})

print(response.json()["data"])
```


# MDS Video

Video Downloader using multithreading and async queue managemet with redis support. Downloads videos to ftp and returns the ftp link and is used by the preprocessing stream.

## Virtual Environment Creation 

Change directory into 
```bash
cd /opt/Virtual_Environments
```

Create the Environment for Video Downloader:
```bash
virtualenv --python=/usr/bin/python3.6 mds_video_env
```
Activate the virtual environment:

```bash
source mds_video_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/MDS_Video/requirements.txt"
```

Download and install Redis Server:

```bash
sudo apt-get install redis-server
sudo systemctl enable redis-server.service
```

Start Redis Server on port `6000`

```bash
redis-server --port 6000 --daemonize yes
```
Ensure that the "command" and "directory" paths in the config file <b>mds_video.conf</b>  are correct. 

```bash
nano /opt/ml_microservices/MDS_Video/mds_video.conf
#make sure the paths to the Virtual Environment and the Microservice app.py are correct
command=/opt/Virtual_Environments/mds_video_env/bin/rq.....
directory=/opt/ml_microservices/MDS_Video/
```

Copy config file from <b>MDS_Video</b> to <b>/etc/supervisor/conf.d/</b> 

```bash
sudo cp /opt/ml_microservices/MDS_Video/mds_video.conf /etc/supervisor/conf.d/
```

Refresh supervisord daemon to load config

```bash
sudo supervisorctl reread
sudo supervisorctl update
```

Run the following command to verify that mds_video service has started

```bash
sudo supervisorctl
```

## Starting the microservice

Create a seperate screen for mds_video

```bash
screen -S MDS_Video
```
Activate the virtual environment:
```bash
source /opt/Virtual_Environments/mds_video_env/bin/activate
```
Change directory into 
```bash
cd /opt/ml_microservices/MDS_Video
```
Run Service (Better to use flask run command for FRS):

```bash
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5007 app:app  
```

Detach Screen 
```bash
CTR + A, D 
```

## Usage

```python
import requests

#send post request on ip and port for MDS_Video from config
response = requests.post(ip:port+"/", json={"video_url": url_str, 'video_name':str_random_name})

""" 
@parameters
video_url: is mandatory

video_name: is optional, if not provided the video will be given random arbitrary name
"""

print(response.json()["url"])
```

# MDS Image

Image downloading using MDS. Downloads images to ftp and returns the ftp link and is used by the preprocessing stream.

## Virtual Environment Creation 

Change directory into 
```bash
cd /opt/Virtual_Environments
```
Create the Environment for MDS_image:

```bash
virtualenv --python=/usr/bin/python3.6 mds_image_env
```
Activate the virtual environment:

```bash
source mds_image_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/MDS_Image/requirements.txt"
```
## Starting the microservice

Create a seperate screen for mds_image

```bash
screen -S MDS_Image
```
Activate the virtual environment:
```bash
source /opt/Virtual_Environments/mds_image_env/bin/activate
```
Change directory into 
```bash
cd /opt/ml_microservices/MDS_Image
```

Run Service

```bash
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5008 app:app 
```

Detach Screen 
```bash
CTR + A, D 
```

## Usage

```python
import requests

#send post request on ip and port for MDS_image from config
response = requests.post(ip:port, json={"imageUrl": image_link})

print(response.json()["url"])
```

# Text Categorization

Text Categorization using zero shot detection

## Virtual Environment Creation 

Change directory into 
```bash
cd /opt/Virtual_Environments
```
Create the Environment for Text Categorization:

```bash
virtualenv --python=/usr/bin/python3.6 cat_env
```
Activate the virtual environment:

```bash
source cat_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/Text_Categorization/requirements.txt"
```
## Starting the microservice

Create a seperate screen for Text Categotization

```bash
screen -S Categorization
```
Activate the virtual environment:
```bash
source /opt/Virtual_Environments/cat_env/bin/activate
```
Change directory into 
```bash
cd /opt/ml_microservices/Text_Categorization
```

Run Service

For Bahrain and Saudiarab

```bash
gunicorn -w 1 -t 10000 --bind 0.0.0.0:5012 app:create_app'("SAUD")'
```

For NRTC

```bash
gunicorn -w 1 -t 10000 --bind 0.0.0.0:5012 app:create_app'("NRTC")'
```

Detach Screen 
```bash
CTR + A, D 
```

## Usage

```python
import requests

#send post request on ip and port for Categorization from config
response = requests.post(ip:port, json={"text": text_in_string,"platform":"twitter"})

print(response.json())
```


# EmoSent

EmoSent is the microservice of Emotion and Sentiment Analysis using zero shot detection.

## Virtual Environment Creation 

Change directory into 
```bash
cd /opt/Virtual_Environments
```
Create the Environment for EmoSent:

```bash
virtualenv --python=/usr/bin/python3.6 emosent_env
```
Activate the virtual environment:

```bash
source emosent_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/EmoSent/requirements.txt"
```
## Starting the microservice

Create a seperate screen for EmoSent

```bash
screen -S EmoSent
```
Activate the virtual environment:
```bash
source /opt/Virtual_Environments/emosent_env/bin/activate
```
Change directory into 
```bash
cd /opt/ml_microservices/EmoSent
```

Run Service

```bash
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5016 app:app 
```

Detach Screen 
```bash
CTR + A, D 
```

## Usage

```python
import requests

#send post request on ip and port for EmoSent from config
response = requests.post(ip:port, json={"text": text_in_string})

print(response.json())
```


# Weapon Object Detection

Weapon Detection model for finding Gun, Pistol, Grenade, and Knife from the Images. 

## Virtual Environment Creation 


Change directory into 
```bash
cd /opt/Virtual_Environments
```

Create the Environment for WOD:

```bash
virtualenv --python=/usr/bin/python3.6 wod_env
```

Activate the virtual environment:

```bash
source wod_env/bin/activate
```

Install torch, torchvision and torch audio for CPU:

```bash
pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
```

Install torch, torchvision and torch audio for GPU:

```bash
pip3 install torch==1.8.2 torchvision==0.9.2 torchaudio==0.8.2 --extra-index-url https://download.pytorch.org/whl/lts/1.8/cu111
```

Install the required packages from requirements.txt:

```bash
pip install -r "../ml_microservices/WOD/requirements.txt"
```


## Starting the microservice

Create a seperate screen for WOD

```bash
screen -S WOD
```
Activate the virtual environment:
```bash
source /opt/Virtual_Environments/wod_env/bin/activate
```
Change directory into 
```bash
cd /opt/ml_microservices/WOD
```

Run Service

```bash
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5017 app:app 
```

Detach Screen 
```bash
CTR + A, D 
```



## Extra (Not necessary to run) 

To Use CPU on GPU Machine for Tensorflow (make changes in app.py)

```bash
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```

## Usage

```python
import requests

#send post request on ip and port for WOD from config
response = requests.post(ip:port/insert, data = {'image_path': image_url_in_string}) # Form Data for text
or
response = requests.post(ip:port/insert, files = {'image_path': image_bytes)}) # Form Data for file
print(response.json()["data"])

```

#### Errors
TypeError: can't convert cuda:0 device type tensor to numpy. Use Tensor.cpu() to copy the tensor to host memory first.

try ---------.cpu().detach().numpy()-------- in load_and_detect() approute insert



# Updating the Virtual Environments
If the Virtual Environment of a microservice needs to be changed due to the change in some requirements, following instructions can be used.

Change directory to the git repository:
```bash
cd /opt/ml_microservices
```
Fetch and pull any updates to the microservices and their requirement files:
```bash
git fetch
git pull
```
Activate the virtual environment that needs to be updated:

```bash
source /opt/Virtual_Environments/<ENV_NAME>/bin/activate
```
Install the New requirements:
```bash
pip install -r "/opt/ml_microservices/<MICROSERVICE_FOLDER>/requirements.txt"
```

# Important Notes

- Do NOT change the folder names of the Virtual Environment folders or any other folder that might be in its path. If changed, the environments will no longer work properly and have to be created again.









