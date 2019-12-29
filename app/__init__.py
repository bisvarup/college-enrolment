from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_dotenv import DotEnv
from flask_migrate import Migrate
import datetime
import sys
import os
from werkzeug.utils import secure_filename
import logging

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../","db")
db_name = "app.db"

sqlite_conn_string = 'sqlite:///' +  os.path.join(basedir, db_name)
print(sqlite_conn_string)


# database configs
app = Flask(__name__, static_folder=os.path.abspath("static/"))
db = None
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_conn_string

# session config
app.secret_key = '51b3d4102d4d0045edbb97fc2fe3e24a10c18fef6ccbeba221dec0868ee28fe7'
app.config['SESSION_TYPE'] = 'filesystem'

# migration script
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# upload folder
UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# enable debug logging
logging.basicConfig(level=logging.DEBUG)

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
