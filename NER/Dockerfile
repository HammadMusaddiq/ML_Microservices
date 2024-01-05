# syntax=docker/dockerfile:1

FROM python:3.6
COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 9001:9001
CMD gunicorn -w 1 -t 10000 --bind 0.0.0.0:9001 app:app

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=7001"]
