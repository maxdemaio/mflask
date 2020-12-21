from flask import Flask
app = Flask(__name__)


@app.route('/')
def home():
    # My home page route
    return 'Hello, World!'

@app.route('/software')
def software():
    # My software page route
    return 'This is my software page!'

# TODO: Create api route for Github projects