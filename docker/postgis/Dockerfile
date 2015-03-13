FROM postgres:9.3
MAINTAINER mdkendall@gmail.com

RUN echo deb http://http.debian.net/debian wheezy-backports main >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y --no-install-recommends \
  postgresql-9.3-postgis-2.1 \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /docker-entrypoint-initdb.d
COPY init-ext.sh /docker-entrypoint-initdb.d/init-ext.sh
