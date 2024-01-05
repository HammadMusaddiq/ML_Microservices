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
Run Service

```bash
gunicorn -w 4 -t 10000 --bind 0.0.0.0:5007 app:app 
```

Detach Screen 
```bash
CTR + A, D 
```

## Extra

To start, stop, or restart supervisord:

```bash
service supervisor start
service supervisor stop
service supervisor restart
```

Run the following command to verify that mds_video service has started:

```bash
sudo supervisorctl
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


