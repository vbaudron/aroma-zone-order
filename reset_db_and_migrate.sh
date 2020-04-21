#!/bin/bash

# Delete DB file
echo "deleting db File..."
rm db.sqlite3

# delete Migrations
echo "deleting migrations..."
cd myapp/migrations
ls | grep "^[0-9]\{4\}_.*py$" | xargs rm
cd ../..

# Create New Migration
echo "make migrations..."
./manage.py makemigrations

# Migrate
echo "migrate..."
./manage.py migrate
