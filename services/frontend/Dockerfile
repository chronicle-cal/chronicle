FROM node:20-alpine AS build
USER node
WORKDIR /app

COPY --chown=node:node services/frontend/package*.json ./
RUN npm ci

COPY --chown=node:node services/frontend ./

RUN NODE_ENV=production npm run build

FROM nginx:stable-alpine
RUN touch /var/run/nginx.pid && \
    chown -R nginx:nginx /var/run/nginx.pid /var/cache/nginx /var/log/nginx /etc/nginx/conf.d


COPY services/frontend/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build --chown=nginx:nginx /app/dist /usr/share/nginx/html

USER nginx

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
