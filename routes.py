from flask import Flask, render_template, url_for , flash, redirect
from __init__ import app, db, bcrypt
from  forms import RegistrationForm, LoginForm
from models import User, Post 

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
        hashed_password = bcrypt.generate_passworf_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for!', 'success')
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