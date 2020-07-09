from flask import Flask, render_template, url_for , flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from  forms import RegistrationForm, LoginForm
from routes.models import User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = '316eae91ff8eb11e29453ae05be9efe6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)