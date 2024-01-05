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
