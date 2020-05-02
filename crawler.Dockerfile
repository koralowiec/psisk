FROM python:3.7-alpine

WORKDIR /code

RUN apk add --no-cache gcc musl-dev libffi-dev libressl-dev linux-headers libxslt-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./static_services .

RUN cd ./static_services

CMD ["scrapy", "crawl", "main"]