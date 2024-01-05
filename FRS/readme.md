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
pip install cmake==3.18.4.post1
```

Install Torch, TorchVision, and TorchAudio packages (CPU):

```bash
pip install torch==1.9.1+cpu torchvision==0.10.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
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
pip install "opencv-python-headless<4.3"
```

Detach Screen 

```bash
CTR + A, D 
```

## To Run Mivlus Docker Image

```bash
sudo docker-compose up -d
```

## Extra (Not necessary to run)  

<<<<<<< Updated upstream
Start Milvus:
=======
Detach Screen 

```bash
CTR + A, D 
```

## To Run Mivlus Docker Image

```bash
sudo docker-compose up -d
```

## Extra (Not necessary to run)  

To Use CPU on GPU Machine for Tensorflow (make changes in app.py)
>>>>>>> Stashed changes

```bash
sudo docker-compose up -d
```

<b>Note:</b> Only use next commands to run/test Milvus docker image in same/separate screen. Run these commands carefully. Start Docker Image in the same frs_milvus path. 

To Start Milvus:

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

Stop Milvus:

```bash
sudo docker-compose down
```

To delete after stoping milvus:

```bash
sudo rm -rf  volumes
```

List all running docker images on the system:

```bash
sudo docker container ls
```

Run Service (Start Milvus):

```bash
screen -S FRS_Milvus
sudo docker-compose up -d
```

## Usage

```python
import requests

#send post request on ip and port for FR from config
response = requests.post(ip:port, json={"imageUrl": single_image_url_string})

print(response.json()["data"])
```
