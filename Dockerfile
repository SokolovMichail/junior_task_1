FROM python:3.10-bookworm

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

RUN pip3 install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system

WORKDIR app