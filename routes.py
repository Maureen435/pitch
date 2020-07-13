import os 
import secrets
from PIL import Image
from flask import Flask, render_template, url_for , flash, redirect
from __init__ import app, db, bcrypt, login_manager
from  forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from models import User, Post 
from flask_login import login_user, current_user, logout_user, login_required

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
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.quetry.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html',title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data 
        db.session.commit()
        flash('your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_username
        form.email.data = current_user.email 
    image_file = url_for('static', filename='profile.pic/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

    @app.route("/post/new")
    @login_required
    def new_post():
        form = PostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('your post has been created!', 'success')
            return redirect(url_for('home'))
        return render_template('create_post.html', title='New post')

    @app.route("/post/<post_id>")
    def post(post_id):
        post = Post.query.get_or_404(post_id)
        return render_template('post.html', title=post.title, post=post)