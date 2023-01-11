#! /bin/bash

python manage.py migrate
run python manage.py createsuperuser --noinpu
python manage.py runserver 0.0.0.0:8000

exec "$@"
