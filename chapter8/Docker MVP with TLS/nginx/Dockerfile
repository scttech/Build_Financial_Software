FROM nginx:latest

EXPOSE 80 443

WORKDIR /etc/nginx

RUN apt-get update && \
    apt-get install -y openssl

RUN mkdir -p /etc/ssl/certs
RUN mkdir -p /etc/ssl/private
RUN chmod 700 /etc/ssl/private

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/localhost.key -out /etc/ssl/certs/localhost.crt \
    -subj "/C=US/ST=YourState/L=YourCity/O=YourOrganization/OU=YourUnit/CN=localhost"

COPY ./dashboard.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]