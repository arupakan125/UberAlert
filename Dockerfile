FROM ubuntu:focal

COPY ./requirements.txt ./

RUN apt-get update && apt-get install -y \ 
    python3 \
    python3-pip \
    git

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY ./app /app

COPY /docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
EXPOSE 3000

ENTRYPOINT ["/docker-entrypoint.sh"]