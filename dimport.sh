#!/bin/sh

if [ ! `type "docker-compose" > /dev/null` ]; then
	. ./docker/windows-init
fi

docker-compose run django ./import_permits.py $@
