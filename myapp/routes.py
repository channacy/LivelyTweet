from app import app, db
from flask import request, render_template, flash, redirect,url_for
from models import User, Tweet
from forms import RegistrationForm,LoginForm
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from datetime import datetime
from authlib.integrations.flask_client import OAuth
from helper import predictLocation, predictSentiment, predictVirality

@app.route('/', methods=["GET", "POST"])
def index():
    location = "--"
    virality = "--"
    sentiment = "--"
    if request.method == 'POST':
      tweet = str(request.form['tweet_value'])
      location = predictLocation(tweet)
      virality = predictVirality(tweet)
      sentiment =  predictSentiment(tweet)
    return render_template('index.html', location = location, virality=virality, sentiment=sentiment)

@app.route("/news")
def news():
  return render_template('news.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  #check if current_user logged in, if so redirect to a page that makes sense
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
  #check if current_user logged in, if so redirect to a page that makes sense
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #change this to match new parameters
        user = User(username=form.username.data, email=form.email.data, followersCount=form.followersCount.data, friendsCount = form.friendsCount.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# @app.route('/user/<username>',methods=['GET', 'POST'])
# @login_required
# def user(username):
# 	user = current_user
# 	user = User.query.filter_by(username=user.username).first()
# 	posts = Post.query.filter_by(user_id=user.id)
# 	if posts is None:
# 		posts = []
# 	form = DestinationForm()
# 	if request.method == 'POST' and form.validate():
# 		new_destination = Post(city = form.city.data,country=form.country.data,description=form.description.data, user_id=current_user.id)
# 	