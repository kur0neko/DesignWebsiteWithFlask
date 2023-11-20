from flask import render_template
from flask import redirect
from flask import flash
from app import myapp_obj
from app.models import User
from app import db

@myapp_obj.route("/")
def index():
	return render_template('index.html')

@myapp_obj.route("/home")
def home():
	return render_template('base.html')

@myapp_obj.route("/login")
def login():
	return render_template('login.html')

@myapp_obj.route("/createaccount")
def createaccount():
	return render_template('createaccount.html')

@myapp_obj.route("/profile")
def profile():
        return render_template('profile.html')


