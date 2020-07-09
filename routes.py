from datetime import datetime
from flask import Flask, render_template, url_for , flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from  forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '316eae91ff8eb11e29453ae05be9efe6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

posts = [
    {
        'author': 'Memzo',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': 'July 7, 2020'
    },
    {
        'author': 'Kemei',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'July 8, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register")
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'memo@gmail.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html',title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)