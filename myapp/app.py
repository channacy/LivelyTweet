from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo_text = db.Column(db.String(100), index = True)

class TodoForm(FlaskForm):
    todo = StringField("Todo")
    submit = SubmitField('Add Todo')

with app.app_context():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def index():
    if 'todo' in request.form:
        db.session.add(Todo(todo_text = request.form['todo']))
        db.session.commit()
    return render_template('index.html', todos = Todo.query.all(), template_form = TodoForm())