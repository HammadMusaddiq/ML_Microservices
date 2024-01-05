FROM python:3.6

COPY . /app

WORKDIR /app

COPY config.ini /
RUN apt-get update -y
RUN apt-get install redis-server -y
RUN apt-get update && apt-get install -y supervisor

COPY mds_video.conf /etc/supervisor/conf.d/mds_video.conf
CMD ["/usr/bin/supervisord"]



#RUN systemctl enable redis-server.service

RUN pip3 install -r requirements.txt
RUN pip3 install torch==1.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip3 install torchvision==0.11.2+cpu torchaudio==0.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN python -m pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html


#EXPOSE 6000
#CMD redis-server --port 6000 --daemonize yes


