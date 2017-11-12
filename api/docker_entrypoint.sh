#! /bin/bash

# Set up remaining migrations
python3 manage.py collectstatic --noinput;

# Boot up the app.
gunicorn oauth_microservice.wsgi --bind=0.0.0.0:8000 --reload;
