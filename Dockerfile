FROM ubuntu:focal

COPY ./requirements.txt ./

RUN apt-get update && apt-get install -y \ 
    python3 \
    python3-pip \
    git

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY ./app /app

EXPOSE 3000
