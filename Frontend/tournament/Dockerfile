FROM node:20-alpine

WORKDIR /app
ARG REACT_APP_API_URL

ENV REACT_APP_API_URL=$REACT_APP_API_URL
COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build
EXPOSE 3000

CMD echo "REACT_APP_API_URL: $REACT_APP_API_URL" && \
    npm start