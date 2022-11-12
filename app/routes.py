from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, PublishForm
from app.models import Post
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import login
from app import db
from app.forms import RegistrationForm

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/index')
@app.route('/')
@login_required
def index():
    articles = Post.query.all()
    return render_template("index.html", title="Home", articles=articles)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/publish', methods=['GET', 'POST'])
@login_required
def publish():
    form = PublishForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user.username)
        db.session.add(post)
        db.session.commit()
        flash('Posted')
        return redirect('/index')
    return render_template('publish.html', title='Publish an article', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/post/<aid>")
def post(aid):
    post = Post.query.get(aid)
    return render_template("post.html", title=post.title, post=post)