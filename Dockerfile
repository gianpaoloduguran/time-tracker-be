FROM python:3.11

ENV LANG C.UTF-8

RUN adduser django

RUN apt-get -y update
RUN apt-get install -y python3-pip python3-dev default-libmysqlclient-dev build-essential mat2=0.13.3-1 ffmpeg libimage-exiftool-perl

ADD ./requirements /home/django/requirements
RUN pip3 install -r /home/django/requirements/requirements.txt

RUN apt-get -y autoremove
WORKDIR /home/django


USER django
