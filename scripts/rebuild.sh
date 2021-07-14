#! /bin/bash
rm -rf ./migrations
./rebuild_db.sh

export FLASK_APP=./app.py
flask db init
flask db migrate
flask db upgrade

# python3 manage.py db init
# python3 manage.py db migrate
# python3 manage.py db upgrade
