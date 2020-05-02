FROM node:12-alpine

WORKDIR /code

COPY ./serving/package*.json ./

RUN npm ci

COPY ./serving/* ./

CMD [ "npm", "start" ]