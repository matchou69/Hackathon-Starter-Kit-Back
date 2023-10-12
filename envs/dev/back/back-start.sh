#!/bin/bash

pg_isready -d ${DB_NAME} -h postgres -p 5432 -U postgres
while [[ $? -ne 0 ]] ; do
  echo "Waiting for postgres server ready to accept connections..."
  sleep 2
  pg_isready -d ${DB_NAME}  -h postgres -p 5432 -U postgres
done

echo "Postgres server ready to accept connections, starting flask server"


export FLASK_APP=main.py
#if [ $MIGRATION == 1 ]; then
#  flask db migrate
#  flask db upgrade
#fi
#uwsgi --enable-threads --ini app/uwsgi.ini
#bandit -r .
# python -m debugpy --listen localhost:5678 --wait-for-client app/main.py

if [ "$TEST_MODE" == "true" ]; then
    pytest -p no:warnings
    exit $?
else
    python app/main.py
fi

