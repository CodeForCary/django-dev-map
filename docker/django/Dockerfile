FROM debian:wheezy
MAINTAINER mdkendall@gmail.com

RUN apt-get update && apt-get install -y \
	python-virtualenv \
	libxml2-dev \
	libxslt-dev \
	libgdal-dev \
	python-dev

RUN mkdir -p /django-install
COPY requirements.txt /django-install/requirements.txt
RUN pip install -r /django-install/requirements.txt

WORKDIR /django
