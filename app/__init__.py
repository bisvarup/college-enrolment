from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_dotenv import DotEnv
import datetime
import sys

app = Flask(__name__)
db = None
try:
    print("Trying to connect to database")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/db'


    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    db = SQLAlchemy(app)
    class User(db.Model):
        __tablename__ = "users"
        id = db.Column('user_id',db.Integer , primary_key=True)
        username = db.Column('username', db.String(20), unique=True , index=True)
        password = db.Column('password' , db.String(10))
        email = db.Column('email',db.String(50),unique=True , index=True)
        registered_on = db.Column('registered_on' , db.DateTime)

        def __init__(self , username ,password , email):
            self.username = username
            self.password = password
            self.email = email
            self.registered_on = datetime.datetime.utcnow()

        def is_authenticated(self):
            return True

        def is_active(self):
            return True

        def is_anonymous(self):
            return False

        def get_id(self):
            return str(self.id)

        def __repr__(self):
            return '<User %r>' % (self.username)

    print("Connected to database")
except:
    print("Error Connecting to database!")

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
from app import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
