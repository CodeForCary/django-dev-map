#!/bin/sh

# This ia a bit of a hack. The postgres image doesn't bring the database up 
# until *after* all initialization has been done (for some reason). Normally
# you would set up the database using "single-user" mode. BUT, you can't 
# create extensions in single user mode, and that's exactly what we need to 
# do in order to make postgis work.
#
# So..we hack.

# Recursively call the script that starts up postgres. The second time this 
# is called, it will just start the databaes. Start it in the background so
# that we can use it.
/docker-entrypoint.sh postgres &

# Wait for the server to start. pg_ctl returns 0 when the database is finally
# up, so is a great thing to wait on, but we can't run it as root. So run it 
# as the postgres user.
until su postgres -c "$(which pg_ctl) status" > /dev/null
do
  sleep 1;
done

# Now we have a database. Create the extension!
psql -h localhost -p 5432 -U $POSTGRES_USER <<- EOSQL
  CREATE EXTENSION IF NOT EXISTS postgis;
  CREATE EXTENSION IF NOT EXISTS unaccent;
EOSQL

# Now shut down the database so that the parent postgres image can start it.
su postgres -c "$(which pg_ctl) stop"
