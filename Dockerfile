FROM ubuntu:16.04

ENV RAPGOD ENV=developpement

WORKDIR /usr/local/src

COPY ai /usr/local/src/ai
COPY data /usr/local/src/data
COPY server /usr/local/src/server
COPY requirements.txt /usr/local/src/requirements.txt
COPY run.sh /usr/local/src/run.sh

RUN apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

RUN chmod u+x run.sh

EXPOSE 80/tcp
