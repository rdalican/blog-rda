import os
import re
import socket
from datetime import datetime, timezone
from flask import Flask, render_template, url_for, flash, redirect, request, session, send_from_directory
from flask_mail import Mail, Message
from dotenv import load_dotenv
from notion_manager import NotionManager
from bs4 import BeautifulSoup
import resend

# Load environment variables from .env files
# Construct the full path to the .env files
# This ensures they are found in both local and production environments
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'Config_Email.env'))
load_dotenv(os.path.join(basedir, 'Config_Notion.env'))

# --- App Initialization and Configuration ---
app = Flask(__name__)

# IMPORTANT: SECRET_KEY must be set in production environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_secret_key')

# Production/Development mode detection
IS_PRODUCTION = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PRODUCTION')
if IS_PRODUCTION:
    app.config['DEBUG'] = False
    print("--- RUNNING IN PRODUCTION MODE ---")
else:
    app.config['DEBUG'] = True
    print("--- RUNNING IN DEVELOPMENT MODE ---")

# --- Dynamic SERVER_NAME for correct URL generation ---
# Check if running on PythonAnywhere by looking for a specific environment variable
# if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    # Production environment on PythonAnywhere
    #public_url = os.getenv('PUBLIC_URL')
    #if public_url:
        #app.config['SERVER_NAME'] = public_url
        #print(f"--- SERVER_NAME configured for PRODUCTION: {app.config['SERVER_NAME']} ---")
    #else:
        # Fallback to the domain provided by PythonAnywhere itself
        #app.config['SERVER_NAME'] = os.environ['PYTHONANYWHERE_DOMAIN']
        #print(f"--- WARNING: PUBLIC_URL not set. Falling back to PythonAnywhere domain: {app.config['SERVER_NAME']} ---")
#else:
    # Local development environment
    #try:
        #hostname = socket.gethostname()
        #local_ip = socket.gethostbyname(hostname)
        # NOTE: This assumes the server runs on port 5000.
        #app.config['SERVER_NAME'] = f"{local_ip}:5000"
        #print(f"--- SERVER_NAME configured for LOCAL DEV: {app.config['SERVER_NAME']} ---")
        #print(f"--- Access the app via http://{local_ip}:5000 from any device on the network. ---")
    #except Exception as e:
        #print(f"--- WARNING: Could not determine local IP. Falling back to localhost. ---")
        #app.config['SERVER_NAME'] = '127.0.0.1:5000'


# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))  # Changed to 465 for SSL
app.config['MAIL_USE_TLS'] = False  # Disable TLS
app.config['MAIL_USE_SSL'] = True   # Enable SSL instead
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_RECIPIENT'] = os.environ.get('MAIL_RECIPIENT')

mail = Mail(app)

# Resend Configuration
resend.api_key = os.environ.get('RESEND_API_KEY')

# Helper function to send email via Gmail SMTP
def send_email_gmail(to_email, subject, html_content):
    """Send email using Gmail SMTP via Flask-Mail"""
    try:
        from flask_mail import Message

        msg = Message(
            subject=subject,
            recipients=[to_email],
            html=html_content,
            sender=app.config['MAIL_DEFAULT_SENDER']
        )

        mail.send(msg)
        print(f"[GMAIL] Email sent successfully to {to_email}", flush=True)
        return True, "Email sent via Gmail"
    except Exception as e:
        print(f"[GMAIL] Failed to send email: {e}", flush=True)
        return False, str(e)

# Helper function to send email via Resend
def send_email_resend(to_email, subject, html_content):
    """Send email using Resend API"""
    try:
        from_email = os.environ.get('MAIL_DEFAULT_SENDER', 'onboarding@resend.dev')

        params = {
            "from": from_email,
            "to": [to_email],
            "subject": subject,
            "html": html_content
        }

        response = resend.Emails.send(params)
        print(f"[RESEND] Email sent successfully. ID: {response.get('id')}", flush=True)
        return True, response
    except Exception as e:
        print(f"[RESEND] Failed to send email: {e}", flush=True)
        return False, str(e)

# Unified email sending function with fallback
def send_email(to_email, subject, html_content):
    """Send email using available provider (Resend or Gmail SMTP)"""
    # Try Resend first if API key is configured
    if os.environ.get('RESEND_API_KEY'):
        success, response = send_email_resend(to_email, subject, html_content)
        if success:
            return True, response
        print(f"[EMAIL] Resend failed, trying Gmail SMTP fallback...", flush=True)

    # Fallback to Gmail SMTP
    return send_email_gmail(to_email, subject, html_content)

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
    message_content = request.form.get('message')
    url = request.form.get('url')
    parent_id = request.form.get('parent_id')

    if not name or not email or not message_content:
        flash('Name, email, and message are required.', 'error')
        return redirect(url_for('post', post_slug=post_slug))

    success, data = notion.add_comment(name, email, message_content, post_slug, url, parent_id)

    if success:
        flash('Il tuo commento è in fase di approvazione dal moderatore del sito.', 'success')

        # Genera gli URL manualmente usando PUBLIC_URL per evitare problemi di contesto
        base_url = os.environ.get('PUBLIC_URL', 'https://blog-rda-production.up.railway.app')
        approve_url = f"{base_url}/approve/{data['approve_token']}"
        delete_url = f"{base_url}/delete/{data['delete_token']}"

        # Ottieni il titolo del post
        post_title = 'Articolo sconosciuto'
        try:
            post_success, post_data = notion.get_post_by_slug(post_slug)
            if post_success and post_data:
                post_title = post_data.get('title', f'Post {post_slug}')
        except Exception as e_post:
            app.logger.warning(f"Could not fetch post title for email: {e_post}")
            post_title = f'Post {post_slug}'

        # Invia email di moderazione in background (non bloccante)
        def send_email_async(name, email, post_title, message_content, approve_url, delete_url):
            print(f"[EMAIL THREAD] Starting email send for comment by {name}", flush=True)
            try:
                print(f"[EMAIL THREAD] Entering app context...", flush=True)
                with app.app_context():
                    print(f"[EMAIL THREAD] Rendering email template...", flush=True)
                    html_content = render_template(
                        'email/moderation_notification.html',
                        name=name,
                        email=email,
                        post_title=post_title,
                        message_content=message_content,
                        approve_url=approve_url,
                        delete_url=delete_url
                    )

                    print(f"[EMAIL THREAD] Sending email to {app.config['MAIL_RECIPIENT']}...", flush=True)
                    success, response = send_email(
                        to_email=app.config['MAIL_RECIPIENT'],
                        subject='💬 Nuovo Commento da Moderare',
                        html_content=html_content
                    )

                    if success:
                        print(f"[EMAIL THREAD] ✅ Email sent successfully for comment by {name}", flush=True)
                    else:
                        print(f"[EMAIL THREAD] ❌ Email failed: {response}", flush=True)
            except Exception as e:
                print(f"[EMAIL THREAD] ❌ Failed to send email: {e}", flush=True)
                import traceback
                print(f"[EMAIL THREAD] Full traceback: {traceback.format_exc()}", flush=True)

        # Avvia thread per invio email in background
        print(f"[MAIN] About to start email thread for comment by {name}", flush=True)
        from threading import Thread
        email_thread = Thread(target=send_email_async, args=(name, email, post_title, message_content, approve_url, delete_url))
        email_thread.daemon = True
        print(f"[MAIN] Starting email thread...", flush=True)
        email_thread.start()
        print(f"[MAIN] Email thread started successfully", flush=True)
    else:
        flash('There was an error submitting your comment.', 'error')

    return redirect(url_for('post', post_slug=post_slug))

@app.route('/approve/<string:token>')
def approve_comment(token):
    if not notion:
        flash('Notion integration is not configured.', 'error')
        return render_template('moderation_result.html', success=False, message='Notion integration is not configured.')
    
    success, comment_page = notion.get_comment_by_token(token)
    if not success or not comment_page:
        return render_template('moderation_result.html', success=False, message='Invalid or expired moderation link.')

    comment_id = comment_page['id']
    update_success, _ = notion.update_comment_status(comment_id, 'Approvato')

    if update_success:
        return render_template('moderation_result.html', success=True, message='Comment approved successfully.')
    else:
        return render_template('moderation_result.html', success=False, message='Failed to approve comment.')

@app.route('/delete/<string:token>')
def delete_comment(token):
    if not notion:
        return render_template('moderation_result.html', success=False, message='Notion integration is not configured.')

    success, comment_page = notion.get_comment_by_token(token)
    if not success or not comment_page:
        return render_template('moderation_result.html', success=False, message='Invalid or expired moderation link.')

    comment_id = comment_page['id']
    update_success, _ = notion.update_comment_status(comment_id, 'Eliminato')

    if update_success:
        return render_template('moderation_result.html', success=True, message='Comment deleted successfully.')
    else:
        return render_template('moderation_result.html', success=False, message='Failed to delete comment.')

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

@app.route('/downloads', methods=['GET', 'POST'])
def downloads():
    if request.method == 'POST':
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        email = request.form.get('email')

        if not nome or not cognome or not email:
            flash('Tutti i campi sono obbligatori.', 'error')
            return render_template('downloads.html', download_ready=False)

        # Save to Notion
        success, message = notion.add_download_request(nome, cognome, email)
        if not success:
            flash(f'Errore nel salvataggio dei dati: {message}', 'error')
            return render_template('downloads.html', download_ready=False)

        # Invia email di notifica download in background (non bloccante)
        def send_download_email_async():
            try:
                with app.app_context():
                    data_ora = datetime.now().strftime('%d/%m/%Y alle %H:%M')

                    html_content = render_template(
                        'email/download_notification.html',
                        nome=nome,
                        cognome=cognome,
                        email=email,
                        data=data_ora
                    )

                    success, response = send_email(
                        to_email=app.config['MAIL_RECIPIENT'],
                        subject='📥 Nuova Richiesta Download - Sistematica Commerciale',
                        html_content=html_content
                    )

                    if success:
                        print(f"[DOWNLOAD EMAIL] ✅ Email sent for {nome} {cognome}", flush=True)
                    else:
                        print(f"[DOWNLOAD EMAIL] ❌ Failed: {response}", flush=True)
            except Exception as e:
                print(f"[DOWNLOAD EMAIL] ❌ Error: {e}", flush=True)

        # Avvia thread per invio email in background
        from threading import Thread
        email_thread = Thread(target=send_download_email_async)
        email_thread.daemon = True
        email_thread.start()

        # Mostra il link per il download
        return render_template('downloads.html', download_ready=True)

    return render_template('downloads.html', download_ready=False)

@app.route('/download_sistematica')
def download_sistematica():
    try:
        return send_from_directory(
            directory=os.path.join(app.root_path, 'static', 'files'),
            path='Sistematica_Commerciale_dist.zip',
            as_attachment=True
        )
    except FileNotFoundError:
        flash('ERRORE CRITICO: Il file per il download non è stato trovato sul server. Contattare il supporto.', 'error')
        return redirect(url_for('downloads'))
    
@app.route('/debug_list_files')
def debug_list_files():
    print("DEBUG: /debug_list_files route called", flush=True)
    files_dir = os.path.join(app.root_path, 'static', 'files')
    try:
        files = os.listdir(files_dir)
        return '<br>'.join(files)
    except Exception as e:
        return f"Errore nell'accesso alla cartella: {e}"
    
# --- Admin Routes ---
def is_admin():
    return session.get('is_admin', False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.environ.get('ADMIN_PASSWORD', 'admin'):
            session['is_admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Password errata.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('login'))
    
    success, posts = notion.get_blog_posts()
    if not success:
        flash('Could not retrieve blog posts.', 'error')
        posts = []
        
    return render_template('admin_dashboard.html', posts=posts)

@app.route('/admin/post/new', methods=['GET', 'POST'])
def admin_new_post():
    if not is_admin():
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Titolo e contenuto sono obbligatori.', 'error')
            return render_template('admin.html', action_url=url_for('admin_new_post'))

        # --- Process HTML to create absolute image URLs ---
        soup = BeautifulSoup(content, 'html.parser')
        images = soup.find_all('img')

        # Determine base URL based on environment
        base_url = os.environ.get('PUBLIC_URL', 'https://rdalican.pythonanywhere.com')

        for img in images:
            src = img.get('src')
            if src and src.startswith('/'):
                img['src'] = f"{base_url}{src}"

        processed_content = str(soup)

        # Determine the next Post ID
        success, posts = notion.get_blog_posts()
        next_post_id = str(len(posts) + 1) if success else "1"

        success, result = notion.add_blog_post(
            title=title,
            html_content=processed_content,
            status="Pubblicato",
            post_id_slug=next_post_id
        )

        if success:
            flash('Post creato con successo!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash(f'Errore durante la creazione del post: {result}', 'error')
            return render_template('admin.html', action_url=url_for('admin_new_post'))

    return render_template('admin.html', action_url=url_for('admin_new_post'))

@app.route('/admin/post/edit/<string:post_id>', methods=['GET', 'POST'])
def admin_edit_post(post_id):
    if not is_admin():
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title or not content:
            flash('Titolo e contenuto sono obbligatori.', 'error')
            return redirect(url_for('admin_edit_post', post_id=post_id))

        # --- Process HTML to create absolute image URLs ---
        soup = BeautifulSoup(content, 'html.parser')
        images = soup.find_all('img')

        # Determine base URL based on environment
        base_url = os.environ.get('PUBLIC_URL', 'https://rdalican.pythonanywhere.com')

        for img in images:
            src = img.get('src')
            if src and src.startswith('/'):
                img['src'] = f"{base_url}{src}"

        processed_content = str(soup)

        # Update content
        notion.update_post_content(post_id, processed_content)
        
        # Update title
        properties = {"Titolo": {"title": [{"text": {"content": title}}]}}
        notion.update_post_properties(post_id, properties)

        flash('Post aggiornato con successo!', 'success')
        return redirect(url_for('admin_dashboard'))

    success, post_data = notion.get_post_by_id(post_id)
    if not success:
        flash('Post non trovato.', 'error')
        return redirect(url_for('admin_dashboard'))
        
    return render_template('admin.html', post=post_data, action_url=url_for('admin_edit_post', post_id=post_id))

@app.route('/admin/post/delete/<string:post_id>', methods=['POST'])
def admin_delete_post(post_id):
    if not is_admin():
        return redirect(url_for('login'))
        
    success, _ = notion.delete_post(post_id)
    if success:
        flash('Post eliminato con successo.', 'success')
    else:
        flash('Errore durante l\'eliminazione del post.', 'error')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = file.filename
        filepath = os.path.join(app.root_path, 'static', 'images', filename)
        file.save(filepath)
        return {'location': f'/static/images/{filename}'}

if __name__ == '__main__':
    # For local development only
    # In production, Gunicorn will handle this
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=not IS_PRODUCTION)


@app.route('/test_copilot')
def test_copilot():
    print("DEBUG: Test Copilot route called", flush=True)
    return "Test Copilot OK"