FROM node:24-alpine

WORKDIR /client_side

COPY package*.json ./

RUN npm install

COPY astro.config.* ./
COPY tsconfig.json ./

COPY . .

RUN npm rebuild

EXPOSE 4321

CMD ["npx", "astro", "dev", "--host", "0.0.0.0", "--port", "4321"]