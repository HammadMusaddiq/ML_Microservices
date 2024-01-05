#Dockerfile
FROM nvcr.io/nvidia/pytorch:22.06-py3
COPY . /app
WORKDIR /app

RUN apt update

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 9003

CMD gunicorn -w 1 -t 10000 --bind 0.0.0.0:9003 app:app


