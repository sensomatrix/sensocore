FROM python:latest
ENV LANG C.UTF-8

RUN mkdir /django

RUN apt-get -y update
RUN apt-get install -y python python-pip python-dev python-psycopg2 postgresql-client 

ADD requirements.txt /django/requirements.txt
RUN pip install -r /django/requirements.txt

RUN apt-get -y update && apt-get -y autoremove
WORKDIR /django

EXPOSE 8000