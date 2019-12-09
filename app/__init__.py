from flask import Flask
from flask_dotenv import DotEnv

app = Flask(__name__)
# Setting up the flask environment from the .flaskenv file
env = DotEnv()

env.init_app(app)

'''
This import is at the bottom to avoid circular dependency
'''
from app import routes
