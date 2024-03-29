from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  friendsCount = db.Column(db.Integer, primary_key=False)
  followersCount = db.Column(db.Integer, primary_key=False)
  tweets = db.relationship('Tweet', backref='author', lazy='dynamic')
  def __repr__(self):
        return '<User {}>'.format(self.username)
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  def check_password(self, password):
    return check_password_hash(self.password_hash, password) 

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String(140))
    predictedLocation = db.Column(db.String(140))
    predictedVirality = db.Column(db.String(140))
    predictedSentiment = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Tweet {}>'.format(self.tweet)

