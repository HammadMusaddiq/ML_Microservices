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