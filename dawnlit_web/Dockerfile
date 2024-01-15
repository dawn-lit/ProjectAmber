# build env
FROM node:20 as node

# set a directory for the app
WORKDIR /app

# copy all the necessary files to the container
COPY ./src ./src
COPY ./angular.json ./
COPY ./package.json ./
COPY ./tsconfig.json ./
COPY ./tsconfig.app.json ./
COPY ./tsconfig.spec.json ./

# install dependencies
RUN npm install

# create a production build
RUN npm run build --prod

# using nginx env
FROM nginx:latest

# COPY nginx cert and key
COPY ./ssl/cert.pem /etc/ssl/cert.pem
COPY ./ssl/key.pem /etc/ssl/key.pem

# copy nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# copy production build
COPY --from=node /app/dist/angular-frontend /usr/share/nginx/html
