# Projektowanie systemów i sieci komputerowych: Projekt

## With Docker

### Build images:

   ```shell
   # image with scrapy
   docker build -f crawler.Dockerfile -t crawler .
   # image with simple expressjs server
   docker build -f serving.Dockerfile -t serving .
   ```

### Start and run containers:
 - with default url:
   ```shell
   # container with crawler, bind mounting dir public for saving files
   docker run --rm -v $(pwd)/public:/public crawler
   # container with "server", bind mounting dir public for serving files, on host using port 3000
   docker run --rm -v $(pwd)/public:/public -p 3000:3000 serving
   ```
 - with setting url:
   ```shell
   # container with crawler, environment variable URL - url to crawl
   docker run --rm -v $(pwd)/public:/public --env URL='https://weii.prz.edu.pl/' crawler
   # container with "server", on host using port 8000 and running in background
   docker run --rm -v $(pwd)/public:/public -p 8000:3000 -d serving
   ```

## With Docker Compose

   ```shell
   docker-compose up
   # or with custom url
   URL='https://weii.prz.edu.pl/' docker-compose up
   ```

## Without Docker

### Install dependencies:

1. Python (version 3.* recomended)
   
   ```shell
   # Creating virtual environment with virtualenv (not mandatory, for not messing up with global python dependencies)
   virtualenv -p python3 ./env
   ```
   
   ```shell
   pip install -r requirements.txt 
   ```

2. NodeJS
   
   ```shell
   cd ./serving && npm i
   cd .. # come back to root of project
   ```

### Run crawler

```shell
cd ./static_services

scrapy crawl main
# or with custom url
scrapy crawl main -a URL='https://weii.prz.edu.pl/'

cd .. # come back to root of project
```

### Run server for serving crawled pages

```shell
cd ./serving
npm start
```

## Browsing pages

All servable HTML files are called page.html

Original page: http://kkio.pti.org.pl/2017/pl/o-konferencji/

Page served from our saved pages: localhost:3000/2017/pl/o-konferencji/page.html


