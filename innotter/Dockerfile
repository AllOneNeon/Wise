# pull official base image
FROM python:3

# set work directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN set -ex && pipenv install --deploy --system
# RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# # install dependencies
# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# copy project
COPY . .

CMD python manage.py runserver