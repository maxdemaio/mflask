import os
from github import Github
from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args

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
    return render_template('index.html')

@app.route('/software')
def software():
    """My software page route"""

    # List of repos and their information
    myRepos = []

    ## Fetch Github objects:
    for repo in g.get_user().get_repos():
        # Only fetch public repositories
        if repo.private == False:
            # Create repo key/value pair and add to myRepos:
            # Name, URL, Description, Language, Created at, Forks,
            # Open issues, Size (kb), Star count
            currRepo = {"name": repo.name, "url": repo.html_url, "description": repo.description,
                        "language": repo.language, "creation": repo.created_at, "forks": repo.forks_count,
                        "issues": repo.open_issues_count, "size": repo.size, "stars": repo.stargazers_count}
            myRepos.append(currRepo)

    ## Paginate Github repos
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    def get_repos(offset=0, per_page=10):
        return myRepos[offset: offset + per_page]
    pagination_repos = get_repos()
    pagination = Pagination(page=page, per_page=per_page, total=len(myRepos),
                            css_framework='bootstrap4')

    return render_template('software.html', myRepos=pagination_repos, pagination=pagination)
