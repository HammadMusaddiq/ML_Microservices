#Dockerfile
FROM nvcr.io/nvidia/pytorch:22.06-py3
COPY . /app
WORKDIR /app

COPY config.ini /

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install tzdata

RUN apt install -y \
    python3-pip python3-dev git curl wget unzip \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    libgl1-mesa-glx \
    libgl1 \
    libopencv-dev

RUN pip3 install --upgrade pip

# to handle openmpi error for pytorch
ENV PATH="${PATH}:/opt/hpcx/ompi/bin"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/opt/hpcx/ompi/lib"
RUN apt install -y libopenblas-base libopenmpi-dev libboost-all-dev

# to handle _imagingft C module error
RUN pip3 install python-multipart

RUN pip3 install --upgrade cmake

RUN pip3 install -r requirements.txt 

#EXPOSE 8001
#CMD gunicorn -w 1 -t 10000 --bind 0.0.0.0:8001 app:app
