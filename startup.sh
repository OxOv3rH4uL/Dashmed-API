#!/bin/bash
python Django-API/manage.py makemigrations
python Django-API/manage.py migrate
python Django-API/manage.py runserver 0.0.0.0:8000
