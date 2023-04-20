FROM node:alpine as builder
WORKDIR /app
# Install dependencies
COPY ./tsconfig.json .
COPY ./package.json .
RUN npm install
# Copy the app over
COPY ./public ./public
COPY ./src ./src
RUN npm run build

FROM nginx
EXPOSE 8080
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html