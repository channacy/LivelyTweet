from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login = LoginManager(app)

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

import routes, models

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#   form = RegistrationForm(csrf_enabled=False)
#   if form.validate_on_submit():
#     # define user with data from form here:
#     user = User(username = form.username.data, email = form.email.data)
#     # set user's password here:
#     user.set_password(form.password.data)
#     db.session.add(user)
#     db.session.commit()
#     return redirect("/")
#   return render_template('register.html', title='Register', form=form)

# user loader
# @login_manager.user_loader
# def load_user(user_id):
#   return User.query.get(int(user_id))

# # login route
# @app.route('/login', methods=['GET','POST'])
# def login():
#   form = LoginForm(csrf_enabled=False)
#   if form.validate_on_submit():
#     # query User here:
#     user = User.query.filter_by(email = form.email.data).first()
#     # check if a user was found and the form password matches here:
#     if user and user.check_password(form.password.data):
#       # login user here:
#       login_user(user, remember = form.remember.data)
#       next_page = request.args.get('next')
#       return redirect(next_page) if next_page else redirect(url_for('/', _external=True, _scheme='https'))
#     else:
#       return redirect(url_for('login', _external=True, _scheme='https'))
#   return render_template('login.html', form=form)

# user route
# @app.route('/user/<username>')
# @login_required
# def user(username):
#   user = User.query.filter_by(username=username).first_or_404()
#   return render_template('user.html', user=user)

