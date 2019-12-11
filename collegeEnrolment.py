import os
from app import app, db

basedir = "db"
db_name = "app.db"
db_file_path = os.path.join(basedir, db_name)

print("Checking if database is present ",os.path.isfile(db_file_path))
'''
Check if the db file is present, if is not present then
create database
'''
if not os.path.isfile(db_file_path):
    print("Creating database")
    db.create_all()
