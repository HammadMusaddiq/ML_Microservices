FROM python:3.8
WORKDIR /app
COPY . /app
<<<<<<< HEAD
EXPOSE 8002
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install -r requirements.txt
CMD gunicorn -w 1 -t 10000 --bind 0.0.0.0:8002 app:app 

=======
EXPOSE 9006
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install -r requirements.txt
CMD gunicorn -w 1 -t 10000 --bind 0.0.0.0:9006 app:app
>>>>>>> 879c79e79c4a90e14fbc494e4844af67a0605d46
