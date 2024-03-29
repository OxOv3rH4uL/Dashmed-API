#!/bin/bash
python Dashmed-API/manage.py makemigrations
python Dashmed-API/manage.py migrate
python Dashmed-API/manage.py runserver 0.0.0.0:8000
