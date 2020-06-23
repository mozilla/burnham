FROM python:3.7-slim-buster

LABEL maintainer "Raphael Pierzina <raphael@hackebrot.de>"

RUN python -m venv venv
RUN . venv/bin/activate

RUN python -m pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt

COPY . /usr/src/burnham-bigquery
WORKDIR /usr/src/burnham-bigquery

ENTRYPOINT [ "pytest" ]
