from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dotenv import DotEnv
import sys

app = Flask(__name__)
try:
    print("Trying to connect to database")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/db'
    db = SQLAlchemy(app)
    print("Connected to database")
except:
    print("Error Connecting to database!!")

# Setting up the flask environment from the .flaskenv file
env = DotEnv()

env.init_app(app)

'''
This import is at the bottom to avoid circular dependency
'''
from app import routes
