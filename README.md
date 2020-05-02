# Projektowanie systemów i sieci komputerowych Projekt

## Install dependencies:

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

## Run crawler

```shell
cd ./static_services
scrapy crawl main
cd .. # come back to root of project
```

## Run server for serving crawled pages

```shell
cd ./serving
npm start
```

## Browsing pages

All servable HTML files are called page.html

Original page: http://kkio.pti.org.pl/2017/pl/o-konferencji/

Page served from our saved pages: localhost:3000/2017/pl/o-konferencji/page.html


