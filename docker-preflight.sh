#!/usr/bin/env bash

#
# Quick-and-easy way to locally run all the checks at once
#

set -e

if grep -R "\.set_trace" api/; then
  echo ">>> Found Python debugger in API <<<"
  exit 1
fi

docker-compose run --rm api flake8
docker-compose run --rm api ./manage.py test
