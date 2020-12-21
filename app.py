from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def index():
    # My home page route
    return render_template('index.html')

@app.route('/software')
def software():
    # My software page route
    return render_template('software.html')

# TODO: Create api route for Github projects