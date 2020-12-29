import json, os, redis
from github import Github
from datetime import date, datetime
from flask import Flask, render_template
from flask_static_digest import FlaskStaticDigest

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Intialize app and Redis connection
app = Flask(__name__)
r = redis.Redis.from_url(os.getenv("REDIS_URL"))

# Flask-Static-Digest config
app.config['FLASK_STATIC_DIGEST_GZIP_FILES'] = False
app.config['FLASK_STATIC_DIGEST_HOST_URL'] = 'https://maxdem-mflask.s3.amazonaws.com/'
flask_static_digest = FlaskStaticDigest()
flask_static_digest.init_app(app)


def get_repos():
    """ Return my software repositories from the Redis cache or the Github API"""
    # Check the Redis hashmap for our repos object
    myRepos = r.get(name="myRepos")
    if myRepos is None:
        # Create a Github instance using an access token
        g = Github(os.getenv("GITHUB_TOKEN"))
        updatedRepos = []
        
        # Fetch Github objects (public and non-forked):
        for repo in g.get_user().get_repos():
            if repo.private == False and repo.fork == False:
                currRepo = {"name": repo.name, "url": repo.html_url, "description": repo.description,
                            "language": repo.language, "creation": repo.created_at.date(),
                            "forks": repo.forks_count, "issues": repo.open_issues_count,
                            "size": repo.size, "stars": repo.stargazers_count}
                updatedRepos.append(currRepo)
        # Convert python object to JSON str and save to Redis cache
        json_repos = json.dumps(updatedRepos, indent=4, sort_keys=True, default=str)
        r.set(name="myRepos", value=json_repos, ex=21600)
        return updatedRepos
    else:
        # Read saved JSON str from Redis and unpack into Python object
        myRepos = json.loads(myRepos.decode('utf-8'))
        return myRepos


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html', now=datetime.utcnow()), 404

@app.route('/')
def index():
    """My home page route"""
    return render_template('index.html', now=datetime.utcnow())

@app.route('/software')
def software():
    """My software page route"""
    # List of repos and their information from cache or Github API
    myRepos = get_repos()
    return render_template('software.html', myRepos=myRepos, now=datetime.utcnow())

if __name__ == '__main__':
    app.run()
