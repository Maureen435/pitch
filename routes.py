import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for , flash, redirect, request, abort
from __init__ import app, db, bcrypt
from  forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from models import User, Post, Comment, Upvote, Downvote 
from flask_login import login_user, current_user, logout_user, login_required


#posts = [
#{
         #   'author': 'Memzo',
    #    'title': 'Blog post 1',
   #     'content': 'First post content',
  #      'date_posted': 'July 7, 2020'
 #   },
#    {
     #   'author': 'Kemei',
    #    'title': 'Blog post 2',
   #     'content': 'Second post content',
  #   }
#]

@app.route("/")
@app.route("/home")
def home():
    title = 'Posts'
    general = Post.query.all()
    product_pitch = Post.query.filter_by(category = 'Product Pitch').all()
    pickup_lines = Post.query.filter_by(category = 'Pickup Lines').all()
    Interview_Pitch = Post.query.filter_by(category = 'Interview Pitch').all()
    Promotion_pitch = Post.query.filter_by(category = 'Promotion Pitch').all()

    return render_template('home.html', title=title, general=general, product_pitch=product_pitch, pickup_pitch=pickup_pitch, interview_pitch=interview_pitch, promotion_pitch=promotion_pitch)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
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

@app.route("/login", methods=['GET', 'POST'])
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

def save_picture(form_picture):
    random_hex = decrets.token_hex(8)
    _, f_ext = os.path.splittext(form_picture.filename)
    picture_fn = random_hex + f_ext 
    picture_path = os.path.join(root_path, 'static/profile.pic', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file 
            current_user.username = form.username.data
            current_user.email = form.email.data 
            db.session.commit()
            flash('Your account has been updated', 'success')
            return redirect(url_for('account'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email 

    image_file = url('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(Post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data)
        db.session.add(comment)
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('home'))
    return render_template('post.html' title=title, post=post, form=form)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
        form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data 
        db.session.commit()
        flash('Your post has been updates', 'success')
        return redirect(url_for('Post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content 
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('home'))