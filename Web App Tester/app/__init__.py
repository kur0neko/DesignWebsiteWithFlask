from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

myapp_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj.config.from_mapping(
    SECRET_KEY = 'thisiscool',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 
'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    GOOGLE_TRANSLATE_SECRET_KEY='insertKeyHere'   #API key goes here, to be used for google translate API. (if more than 60,000 characters get translated in a month, I get charged money)
)

db = SQLAlchemy(myapp_obj)

with myapp_obj.app_context():
    from app.models import User, Note, Table
    db.create_all()

from app import routes
