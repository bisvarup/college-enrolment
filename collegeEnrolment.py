import os
from app import app, db

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../","db")
db_name = "app.db"
db_file_path = os.path.join(basedir, db_name)

print("Is db file present ",os.path.isfile(db_file_path))
'''
Check if the db file is present, if is not present then
create database
'''
if not os.path.isfile(db_file_path):
    db.create_all()

app.debug = True
app.run()

