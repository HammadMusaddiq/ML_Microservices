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
#image_url_in_string = "url1"

print(response.json()["data"])
```