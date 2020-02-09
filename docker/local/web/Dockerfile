# pull official base image
FROM python:3.7-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# Install pipenv
RUN pip install --user pipenv

#COPY ./requirements.txt /usr/src/app/requirements.txt
#RUN pip install -r requirements.txt
COPY ./Pipfile /app
COPY ./Pipfile.lock /app

RUN ~/.local/bin/pipenv install

# copy project
# COPY ../todo_everything /usr/src/app/
