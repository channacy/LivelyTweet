from app import app, db
from flask import request, render_template, flash, redirect,url_for, session
from models import User, Tweet
from forms import RegistrationForm,LoginForm, TweetForm
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
import requests 
from config import NEWS_API_KEY

@app.route('/', methods=["GET", "POST"])
def index():
    form = TweetForm()
    location = "--"
    virality = "--"
    sentiment = "--"
    tweet = None
    if request.form.get('tweet_value'):
        tweet = str(request.form['tweet_value'])
        location = predictLocation(tweet)
        sentiment =  predictSentiment(tweet)
        if current_user.is_authenticated:
            user = current_user
            user = User.query.filter_by(username=user.username).first()
            numFriends = user.friendsCount
            numFollowers = user.followersCount
            virality = predictVirality(tweet,numFollowers, numFriends)
            db.session.add(Tweet(tweet = request.form.get('tweet_value'), predictedLocation = location, predictedVirality = virality,predictedSentiment = sentiment, user_id=current_user.id))
            db.session.commit()
        
    # else:
    #     print("viral", virality)
    #     db.session.add(Tweet(tweet = request.form.get('tweet_value'), predictedLocation = location, predictedVirality = virality,predictedSentiment = sentiment, user_id=current_user.id))
    #     db.session.commit()
    #     print("saved")
    return render_template('index.html',tweet = tweet, location = location, virality=virality, sentiment=sentiment, form = form)

@app.route("/news", methods=["GET"])
def news():
    api_key = NEWS_API_KEY
    base_url = 'https://newsapi.org/v2/top-headlines'
    params = {'country': 'us', 'apiKey': api_key}
    
    response = requests.get(base_url, params=params)
    news_data = response.json().get('articles', [])

    return render_template('news.html', news=news_data)

@app.route("/saved", methods=["GET"])
def savedTweets():       
    user = current_user
    userTweets = Tweet.query.filter_by(user_id=user.id).all()
    return render_template('tweets.html', tweets=userTweets)

@app.route("/profile", methods=["GET"])
def profile():       
  return render_template('profile.html')

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
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