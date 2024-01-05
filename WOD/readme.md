
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

