FROM python:3.7-alpine

WORKDIR /code

ENV URL="http://kkio.pti.org.pl/2017/"

RUN apk add --no-cache gcc musl-dev libffi-dev libressl-dev linux-headers libxslt-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./static_services .

RUN cd ./static_services

# https://stackoverflow.com/a/40454758
CMD ["sh","-c","scrapy crawl main -a url=${URL}"]