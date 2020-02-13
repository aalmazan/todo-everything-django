# pull official base image
FROM python:3.7-slim-buster

RUN useradd --create-home webapp

# set work directory
WORKDIR /home/webapp
USER webapp

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# Install pipenv
RUN pip install --user pipenv
ENV PATH="${PATH}:/home/webapp/.local/bin"

#COPY ./requirements.txt /usr/src/app/requirements.txt
#RUN pip install -r requirements.txt
COPY ./Pipfile /home/webapp
COPY ./Pipfile.lock /home/webapp

# This is a dev version of the Dockerfile, so we also need the dev dependencies
RUN set -ex && /home/webapp/.local/bin/pipenv install --deploy --system --dev

# copy project
# COPY ../todo_everything /usr/src/app/
