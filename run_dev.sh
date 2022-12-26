#!/usr/bin/env bash

# start background tasks

source venv/bin/activate ;
python manage.py runserver &
python manage.py process_tasks
