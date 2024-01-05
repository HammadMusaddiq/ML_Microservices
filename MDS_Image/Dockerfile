
FROM python:3.6

COPY . /app

WORKDIR /app

RUN apt-get update -y
RUN pip3 install -r requirements.txt
RUN pip3 install torch==1.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip3 install torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html

EXPOSE 9003:9003
CMD gunicorn -w 1 -t 10000 --bind 0.0.0.0:9003 app:app
