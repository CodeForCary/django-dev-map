FROM debian:wheezy
MAINTAINER mdkendall@gmail.com

RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_0.12 | bash -
RUN apt-get install -y nodejs git

RUN mkdir -p /django/permit_map/static/permit_map
WORKDIR /django/permit_map/static/permit_map

RUN npm install -g bower
RUN bower --allow-root --config.interactive=false install angular-material#0.8.3 angular-ui-router#0.2.13

CMD bower --allow-root --config.interactive=false update && ping -i 60 127.0.0.1 > /dev/null
