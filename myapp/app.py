from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user
from datetime import datetime
from authlib.integrations.flask_client import OAuth
from helper import predictLocation, predictSentiment, predictVirality
# import pickle 
# from sklearn.preprocessing import scale
# from sklearn.metrics.pairwise import euclidean_distances
# from sklearn.neighbors import KNeighborsClassifier

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
oauth = OAuth(app)

# with open('models/locationClassifier.pkl', 'rb') as location_classifier:
#     locationClassifier = pickle.load(location_classifier)

# with open('models/vectorizer.pkl', 'rb') as vectorizer_file:
#     counter = pickle.load(vectorizer_file)

# with open('models/text_sentiment_vectorizer.pkl', 'rb') as sentiment_text_vectorizer:
#     text_vectorizer = pickle.load(sentiment_text_vectorizer)

# with open('models/sentiment_model.pkl', 'rb') as sentiment_model:
#     NB_classifier = pickle.load(sentiment_model)

# with open('models/virality_model.pkl', 'rb') as virality_model:
#     virality_classifier = pickle.load(virality_model)

# @app.route('/predictLocation',methods=["GET"])
# def predict():
#   tweetExample = "I love this baguette! I am eating one over the Effiel tower in France:)"
#   tweet_counts = counter.transform([tweetExample])
#   prediction = locationClassifier.predict(tweet_counts)
#   if prediction == [0]:
#     location  = "New York"
#   elif prediction == [1]:
#     location = "London"
#   else:
#     location = "Paris"
#   return render_template('predict.html', prediction=location)

# @app.route("/predictPos", methods=["GET"])
# def predictPos():
#    tweetExample = ["I hate cs"]
#    result = text_vectorizer.vectorizer.transform(tweetExample)
#    prediction = NB_classifier.predict(result)
#    if prediction == 0:
#     return "Positive"
#    else:
#     return "Negative"

# @app.route("/getVirality", methods=["GET"])
# def getVirality():
#     tweet_info = [[55, 100000, 1060, 5, 20, 30, 4]]
#     scaled_tweet = scale(tweet_info, axis = 0)
#     print(virality_classifier.predict(scaled_tweet))
#     return "working"
    
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_text = db.Column(db.String(100), index = True)

class TodoForm(FlaskForm):
    todo = StringField("Todo")
    submit = SubmitField('Add Todo')

# create login manager
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), index = True, default = datetime.utcnow)
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  # add email field here:
  email = StringField('Email', validators = [DataRequired(), Email()])
  # add password fields here:
  password = PasswordField('Password', validators = [DataRequired()])
  password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])

  submit = SubmitField('Register')

# login form
class LoginForm(FlaskForm):
  email = StringField('Email',
  validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

with app.app_context():
    db.create_all()

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

# @app.route('/result', methods=["GET"])
# def index():
#     input_value = request.form.get('tweet_value')
#     location = predictLocation(input_value)
#     virality = predictVirality(input_value)
#     sentiment = predictSentiment(input_value)
#     return render_template('index.html', tweet = input_value, location = location, virality=virality, sentiment=sentiment)

@app.route("/news")
def news():
  return render_template('news.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm(csrf_enabled=False)
  if form.validate_on_submit():
    # define user with data from form here:
    user = User(username = form.username.data, email = form.email.data)
    # set user's password here:
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    return redirect("/")
  return render_template('register.html', title='Register', form=form)

# user loader
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

# login route
@app.route('/login', methods=['GET','POST'])
def login():
  form = LoginForm(csrf_enabled=False)
  if form.validate_on_submit():
    # query User here:
    user = User.query.filter_by(email = form.email.data).first()
    # check if a user was found and the form password matches here:
    if user and user.check_password(form.password.data):
      # login user here:
      login_user(user, remember = form.remember.data)
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('/', _external=True, _scheme='https'))
    else:
      return redirect(url_for('login', _external=True, _scheme='https'))
  return render_template('login.html', form=form)

# user route
@app.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('user.html', user=user)

