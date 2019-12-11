from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_dotenv import DotEnv
import datetime
import sys
import os

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../","db")
db_name = "app.db"

sqlite_conn_string = 'sqlite:///' +  os.path.join(basedir, db_name)

app = Flask(__name__)
db = None
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_conn_string
    app.secret_key = '51b3d4102d4d0045edbb97fc2fe3e24a10c18fef6ccbeba221dec0868ee28fe7'
    app.config['SESSION_TYPE'] = 'filesystem'

    db = SQLAlchemy(app)
except:
    print("Error connecting to database! Terminating script....")
    sys.exit()

# Setting up the flask environment from the .flaskenv file
env = DotEnv()
env.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginStudent'


'''
This import is at the bottom to avoid circular dependency
'''
from app import routes
from app.database import Student, Teacher

@login_manager.user_loader
def load_user(id):
    return Student.query.get(int(id)) or Teacher.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
