FROM node:20-alpine

WORKDIR /app

COPY services/frontend/package*.json ./
RUN npm ci

COPY services/frontend ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
