import os
from github import Github
from datetime import datetime
from flask import Flask, render_template

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# Intialize app
app = Flask(__name__)

# Create a Github instance using an access token
g = Github(os.getenv("GITHUB_TOKEN"))

@app.route('/')
def index():
    """My home page route"""
    return render_template('index.html', now=datetime.utcnow())

@app.route('/software')
def software():
    """My software page route"""
    # List of repos and their information
    myRepos = []

    ## Fetch Github objects:
    for repo in g.get_user().get_repos():
        # Only fetch public and non-forked repositories
        if repo.private == False and repo.fork == False:
            # Create repo key/value pair and add to myRepos:
            # Name, URL, Description, Language, Created at, Forks,
            # Open issues, Size (kb), Star count
            currRepo = {"name": repo.name, "url": repo.html_url, "description": repo.description,
                        "language": repo.language, "creation": repo.created_at.date(),
                        "forks": repo.forks_count, "issues": repo.open_issues_count, 
                        "size": repo.size, "stars": repo.stargazers_count}
            myRepos.append(currRepo)

    return render_template('software.html', myRepos=myRepos, now=datetime.utcnow())
