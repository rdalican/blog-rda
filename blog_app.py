import os
import re
from datetime import datetime, timezone
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_mail import Mail, Message
from dotenv import load_dotenv
from notion_manager import NotionManager

# Load environment variables from .env files
# Construct the full path to the .env files
# This ensures they are found in both local and production environments
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'Config_Email.env'))
load_dotenv(os.path.join(basedir, 'Config_Notion.env'))

# --- App Initialization and Configuration ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_secret_key')

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_RECIPIENT'] = os.environ.get('MAIL_RECIPIENT')

mail = Mail(app)

# Notion Manager Initialization
try:
    notion = NotionManager()
except Exception as e:
    print(f"Error initializing Notion Manager: {e}")
    notion = None

# --- Template Filters and Context Processors ---
@app.template_filter('regex_replace')
def regex_replace(s, find, replace=''):
    return re.sub(find, replace, s)

@app.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}

# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    if not notion:
        flash('Notion integration is not configured.', 'error')
        return render_template('blog.html', posts=[])
    
    success, posts = notion.get_blog_posts()
    if not success:
        flash('Could not retrieve blog posts.', 'error')
        return render_template('blog.html', posts=[])
    
    return render_template('blog.html', posts=posts)

@app.route('/post/<string:post_slug>')
def post(post_slug):
    if not notion:
        flash('Notion integration is not configured.', 'error')
        return redirect(url_for('blog'))

    success, post_data = notion.get_post_by_slug(post_slug)
    if not success or not post_data:
        flash('Post not found.', 'error')
        return redirect(url_for('blog'))

    comments_success, comments = notion.get_comments_for_post(post_slug)
    
    return render_template('post.html', post=post_data, comments=comments if comments_success else [])

@app.route('/post/<string:post_slug>/comment', methods=['POST'])
def add_comment_route(post_slug):
    if not notion:
        flash('Notion integration is not configured.', 'error')
        return redirect(url_for('post', post_slug=post_slug))

    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    url = request.form.get('url')
    parent_id = request.form.get('parent_id')

    if not name or not email or not message:
        flash('Name, email, and message are required.', 'error')
        return redirect(url_for('post', post_slug=post_slug))

    success, _ = notion.add_comment(name, email, message, post_slug, url, parent_id)

    if success:
        flash('Your comment has been submitted and is awaiting moderation.', 'success')
    else:
        flash('There was an error submitting your comment.', 'error')

    return redirect(url_for('post', post_slug=post_slug))

@app.route('/moderation')
def moderation():
    if not notion:
        flash('Notion integration is not configured.', 'error')
        return render_template('moderation.html', comments=[])

    success, comments = notion.get_comments_for_moderation()
    if not success:
        flash('Could not retrieve comments for moderation.', 'error')
        return render_template('moderation.html', comments=[])

    return render_template('moderation.html', comments=comments)

@app.route('/moderation/update', methods=['POST'])
def update_comment_status():
    if not notion:
        flash('Notion integration is not configured.', 'error')
        return redirect(url_for('moderation'))

    comment_id = request.form.get('comment_id')
    status = request.form.get('status')
    notes = request.form.get('notes')

    if not comment_id or not status:
        flash('Comment ID and status are required.', 'error')
        return redirect(url_for('moderation'))

    success, _ = notion.update_comment_status(comment_id, status, notes)

    if success:
        flash(f'Comment has been {status}.', 'success')
    else:
        flash('There was an error updating the comment.', 'error')

    return redirect(url_for('moderation'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if not notion:
            flash('Notion integration is not configured.', 'error')
            return redirect(url_for('contact'))

        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        message = request.form.get('message')

        # Add contact to Notion
        notion.add_contact(name, email, message, company)

        # Send email notification
        try:
            msg = Message(
                'New Contact Form Submission',
                recipients=[app.config['MAIL_RECIPIENT']],
                body=f"From: {name} <{email}>\nCompany: {company}\n\n{message}"
            )
            mail.send(msg)
            flash('Thank you for your message. I will get back to you shortly.', 'success')
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Your message was saved, but the notification email could not be sent.', 'warning')

        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

if __name__ == '__main__':
    app.run(debug=True)