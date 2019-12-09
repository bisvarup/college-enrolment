from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_dotenv import DotEnv
import datetime
import sys

app = Flask(__name__)
db = None
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/db'
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    db = SQLAlchemy(app)
except:
    print("Error connecting to database!")

# Setting up the flask environment from the .flaskenv file
env = DotEnv()
env.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


'''
This import is at the bottom to avoid circular dependency
'''
from app import routes
from app.database import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
