#!/bin/bash

pg_isready -d chuut -h 172.31.39.151 -p 5432 -U postgres
while [[ $? -ne 0 ]] ; do
  echo "Waiting for postgres server ready to accept connections..."
  sleep 2
  pg_isready -d chuut -h 172.31.39.151 -p 5432 -U postgres
done

echo "Postgres server ready to accept connections, starting flask server"


export FLASK_APP=main.py
if [ '$MIGRATION' == '1' ]; then
  flask db migrate
  flask db upgrade
fi
uwsgi --enable-threads --ini app/uwsgi.ini
#python app/main.py
#python -m debugpy --listen localhost:5678 --wait-for-client app/main.py
