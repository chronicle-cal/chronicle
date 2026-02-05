# services/frontend/Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies first (better caching)
COPY services/frontend/package*.json ./
RUN npm ci

# Copy source
COPY services/frontend ./

# Vite dev server
EXPOSE 5173

# --host 0.0.0.0 is required to access the dev server from outside the container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
