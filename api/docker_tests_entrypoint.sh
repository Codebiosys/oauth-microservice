#! /bin/bash

echo "[$(date)] Running tests..."
coverage run --branch --source='users' manage.py test

echo "[$(date)] Generating coverage report..."
coverage html -d coverage
