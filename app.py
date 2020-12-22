# Load environment variables
from dotenv import load_dotenv
from github import Github
load_dotenv()

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Intialize app and database (development)
app = Flask(__name__)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    # My home page route
    return render_template('index.html')

@app.route('/software')
def software():
    # My software page route
    return render_template('software.html')
