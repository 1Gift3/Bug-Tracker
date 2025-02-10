import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin

app = Flask(__name__)

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Table
class User(db.Model, UserMixin):
    __tablename__ = 'user'  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"<User {self.username}>"

    # Relationships
    tasks = db.relationship('Task', backref='user', lazy=True)
    quizzes = db.relationship('Quiz', backref='user', lazy=True)

# Task Table (Linked to Users)
class Task(db.Model):
    __tablename__ = 'task' 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.String(10), nullable=False, default='Medium')  # Low, Medium, High
    status = db.Column(db.String(20), nullable=False, default='To-Do')

    def __repr__(self):
        return f"<Tser {self.description}>"
    
# Bug Table (Linked to Users)
class Bug(db.Model):
    __tablename__ = 'bug'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  

    description = db.Column(db.Text, nullable=False)
    steps_to_reproduce = db.Column(db.Text, nullable=False)
    expected_outcome = db.Column(db.Text, nullable=False)
    actual_outcome = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(10), nullable=False, default='Medium')  # Low, Medium, High
    status = db.Column(db.String(20), nullable=False, default='Open')

    
# Quiz Table (Linked to Users)
class Quiz(db.Model):
    __tablename__ = 'quiz'  

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  #

    score = db.Column(db.Integer, nullable=False)
    date_taken = db.Column(db.Date, nullable=False)

    # Relationship
    quiz_questions = db.relationship('QuizQuestion', backref='quiz', lazy=True)

# Question Table
class Question(db.Model):
    __tablename__ = 'question' 

    id = db.Column(db.Integer, primary_key=True)

    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # A, B, C, D

# QuizQuestion Table (Mapping Between Quiz & Questions)
class QuizQuestion(db.Model):
    __tablename__ = 'quiz_question'  

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)  # 
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)  
    selected_option = db.Column(db.String(1), nullable=True)  # A, B, C, D


if __name__ == '__main__':
    app.run(debug=True)