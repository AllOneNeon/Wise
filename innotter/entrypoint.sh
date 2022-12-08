#!/usr/bin/env bash

# python3 manage.py migrate

# python3 manage.py runserver 0.0.0.0:8000

#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

 python manage.py flush --no-input
 python manage.py migrate

 CMD python manage.py runserver
 
exec "$@"