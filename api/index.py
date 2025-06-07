from flask import Flask, render_template, jsonify, abort
import os
from dotenv import load_dotenv
from notion_client import Client
from .notion_helper import get_blog_posts, get_post_by_id
from notion_manager import NotionManager

load_dotenv()

app = Flask(__name__,
           template_folder='../templates',  # Point to templates in parent directory
           static_folder='../static')       # Point to static in parent directory

notion = NotionManager()

@app.route('/api/test')
def test():
    """Test endpoint to verify the application is working"""
    return jsonify({
        "status": "ok",
        "notion_token": "configured" if os.environ.get("NOTION_TOKEN") else "missing",
        "notion_db": "configured" if os.environ.get("NOTION_DATABASE_ID") else "missing"
    })

@app.route('/')
def home():
    try:
        posts = get_blog_posts()
        # Filter only published posts
        published_posts = [post for post in posts if post.get('stato', '').lower() == 'pubblicato']
        return render_template('index.html', posts=published_posts[:3])  # Show latest 3 published posts
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/blog')
def blog():
    try:
        posts = get_blog_posts()
        # Filter only published posts
        published_posts = [post for post in posts if post.get('stato', '').lower() == 'pubblicato']
        return render_template('blog.html', posts=published_posts)
    except Exception as e:
        print(f"Error in blog route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/blog/<post_id>')
def post(post_id):
    try:
        post = get_post_by_id(post_id)
        if not post or post.get('stato', '').lower() != 'pubblicato':
            abort(404)
        return render_template('post.html', post=post)
    except Exception as e:
        print(f"Error in post route: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/contacts')
def get_contacts():
    """Recupera tutti i contatti dal database Notion"""
    try:
        contacts = notion.get_contacts()
        return jsonify(contacts)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments')
def get_all_comments():
    """Recupera tutti i commenti dal database Notion"""
    try:
        comments = notion.get_all_comments()
        return jsonify(comments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comments/<post_id>')
def get_comments_by_post(post_id):
    """Recupera i commenti per un post specifico"""
    try:
        success, comments = notion.get_comments_for_post(post_id)
        if not success:
            return jsonify({'error': comments}), 500
        return jsonify(comments)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For local testing only
if __name__ == '__main__':
    app.run(port=3000, debug=True)