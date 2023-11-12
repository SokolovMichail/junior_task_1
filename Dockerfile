FROM python:3.10-bookworm

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR app

RUN apt-get update

RUN pip3 install pipenv

COPY . .

RUN pipenv install --system

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]