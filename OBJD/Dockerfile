# syntax=docker/dockerfile:1

FROM python:3.6
COPY . /app
WORKDIR /app

RUN apt-get update -y

RUN apt install -y \
    python3-pip python3-dev git curl wget unzip \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    libgl1-mesa-glx \
    libgl1 \
    libopencv-dev

RUN apt-get install gcc -y
RUN pip3 install -r requirements.txt
RUN pip3 install torch==1.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip3 install torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html

RUN pip uninstall pillow -y
RUN apt install -y libfreetype6-dev
RUN pip install pillow python-multipart

Expose 9002:9002
CMD gunicorn -w 1 -t 10000 --bind 0.0.0.0:9002 app:app

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=8001"]
