FROM node:13.12.0-alpine

WORKDIR /usr/src/vilantis/client

COPY package*.json ./

RUN npm ci -qy

COPY . .

EXPOSE 3000

CMD ["npm", "start"]