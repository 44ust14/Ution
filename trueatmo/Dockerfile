FROM python:3
RUN mkdir /trueatmo
WORKDIR /trueatmo
USER root
ADD requirements.txt /trueatmo
RUN pip install -r requirements.txt
ADD . /trueatmo
