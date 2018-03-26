#! /bin/sh

set -e

# Block until pgsql is listening
# Checks 10 times with sleeps in between to ensure that it didn't restart
until (for run in {1..10} ; do nc -z $PG_HOST 5432 && sleep 1; done); do
    echo "Waiting for $PG_HOST to be listening..."
    sleep 3
done

alembic upgrade head;
