from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_dotenv import DotEnv
import sys

app = Flask(__name__)
db = None
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


'''
This import is at the bottom to avoid circular dependency
'''
from app import routes, User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
