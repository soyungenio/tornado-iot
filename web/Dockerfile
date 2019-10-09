FROM python:3.7-alpine

ARG POSTGRES_HOST
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

ENV POSTGRES_HOST=${POSTGRES_HOST}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}

ARG RABBITMQ_DEFAULT_HOST
ARG RABBITMQ_DEFAULT_USER
ARG RABBITMQ_DEFAULT_PASS
ARG RABBITMQ_DEFAULT_VHOST

ENV RABBITMQ_HOST=${RABBITMQ_DEFAULT_HOST}
ENV RABBITMQ_USER=${RABBITMQ_DEFAULT_USER}
ENV RABBITMQ_PASS=${RABBITMQ_DEFAULT_PASS}
ENV RABBITMQ_VHOST=${RABBITMQ_DEFAULT_VHOST}

# set working directory
WORKDIR /usr/src/app

# copy requirements.txt
COPY requirements.txt /usr/src/app/requirements.txt

# install dependencies
RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 pip install --upgrade pip && pip install -r requirements.txt && \
 apk --purge del .build-deps

# add app
COPY . /usr/src/app

RUN chmod +x ./start.sh

EXPOSE 80

ENTRYPOINT sh start.sh