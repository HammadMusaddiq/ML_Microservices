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
response = requests.post(ip:port, json={"text": text_in_string, "platform":"twitter"})

print(response.json())


```


