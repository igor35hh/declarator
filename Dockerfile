FROM python:3.5
ENV PYTHONUNBUFFERED 1

RUN mkdir /declarator

WORKDIR /declarator

ADD requirements.txt /declarator/

ADD . /declarator/

RUN pip install -r /declarator/requirements.txt
