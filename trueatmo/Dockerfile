FROM python:3
RUN mkdir /trueatmo
WORKDIR /trueatmo
ADD requirements.txt /trueatmo
RUN pip install -r requirements.txt
ADD . /trueatmo
