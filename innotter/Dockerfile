FROM python:3.11

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

# RUN DJANGO_SUPERUSER_PASSWORD=123123 python manage.py createsuperuser --noinput admin

# copy project
COPY . /app
RUN chmod +x /app/entrypoint.sh
# CMD ["/app/entrypoint.sh"]
# ENTRYPOINT ["usr/src/app/entrypoint.sh"]
ENTRYPOINT [ "bash", "-c", "./entrypoint.sh" ]