#!/bin/bash
while ! nc -z rabbitmq-server 5672
do
	echo "rabbitmq is unavailable - starting"
	sleep 3
done
python manage.py