FROM node:16-alpine

WORKDIR /probe-ui
COPY package.json .
COPY . .
ENV NODE_ENV=production
RUN yarn install