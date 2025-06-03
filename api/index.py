from flask import Flask, render_template, jsonify, abort
import os
from dotenv import load_dotenv
from notion_client import Client
from .notion_client import get_blog_posts, get_post_by_slug

load_dotenv()

app = Flask(__name__, 
           template_folder='../templates',  # Point to templates in parent directory
           static_folder='../static')       # Point to static in parent directory

@app.route('/')
def home():
    posts = get_blog_posts()
    return render_template('index.html', posts=posts[:3])  # Show latest 3 posts

@app.route('/blog')
def blog():
    posts = get_blog_posts()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def post(slug):
    post = get_post_by_slug(slug)
    if not post:
        abort(404)
    return render_template('post.html', post=post)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok"})

def handler(request):
    """Handle a request to the Flask application."""
    return app(request) 