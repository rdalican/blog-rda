from flask import Flask, render_template, url_for, flash, redirect, request
from datetime import datetime, timezone
import re
from notion_manager import NotionManager
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('Config_Email.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_RECIPIENT'] = os.environ.get('MAIL_RECIPIENT')

mail = Mail(app)

try:
    notion = NotionManager()
except Exception as e:
    print(f"Errore durante l'inizializzazione di Notion: {str(e)}")
    notion = None

@app.template_filter('regex_replace')
def regex_replace(s, find, replace=''):
    """A non-optimal implementation of a regex filter"""
    return re.sub(find, replace, s)

@app.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    if notion is None:
        flash('Configurazione Notion non disponibile. Contatta l\'amministratore.', 'error')
        return render_template('blog.html', posts=[])
    success, posts = notion.get_blog_posts()
    if not success:
        flash('Errore nel recupero dei post. Contatta l\'amministratore.', 'error')
        return render_template('blog.html', posts=[])
    return render_template('blog.html', posts=posts)

@app.route('/post/<string:post_id>')
def post(post_id):
    if notion is None:
        flash('Configurazione Notion non disponibile. Contatta l\'amministratore.', 'error')
        return redirect(url_for('blog'))
    
    # The post_id from the URL is now the Notion Page ID
    success, post_data = notion.get_post_by_id(post_id)
    
    if not success:
        flash('Post non trovato.', 'error')
        return redirect(url_for('blog'))
        
    # We still need the custom slug for comments, so we retrieve it from the post data
    custom_post_slug = post_data.get('post_id', post_id)
    
    success_comments, comments = notion.get_comments_for_post(custom_post_slug)
    
    return render_template('post.html', post=post_data, comments=comments if success_comments else [])

@app.route('/add_comment/<string:post_id>', methods=['POST'])
def add_comment(post_id):
    if notion is None:
        flash('Configurazione Notion non disponibile. Contatta l\'amministratore.', 'error')
        return redirect(url_for('post', post_id=post_id))

    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Get the post title
    success, post = notion.get_post_by_id(post_id)
    if not success:
        flash('Post non trovato.', 'error')
        return redirect(url_for('blog'))
    post_title = post['title']

    success, result = notion.add_comment(name, email, message, str(post_id))

    if success:
        # Send email notification with post title
        try:
            msg = Message(
                f'Nuovo commento sul post: {post_title}',
                recipients=[app.config['MAIL_RECIPIENT']],
                body=f'''Nuovo commento ricevuto:
                
Da: {name} ({email})
Post: {post_title}
Messaggio:
{message}'''
            )
            mail.send(msg)
        except Exception as e:
            print(f"Errore nell'invio dell'email: {str(e)}")

        flash('Grazie per il tuo commento! Verrà pubblicato dopo la moderazione.', 'success')
    else:
        error_msg = f'Errore: {result}' if result else 'Si è verificato un errore durante l\'invio del commento.'
        flash(error_msg, 'error')
        print(f"Errore dettagliato: {result}")

    return redirect(url_for('post', post_id=post_id))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/downloads')
def downloads():
    return render_template('downloads.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if notion is None:
            flash('Configurazione Notion non disponibile. Contatta l\'amministratore.', 'error')
            return redirect(url_for('contact'))

        name = request.form.get('name')
        email = request.form.get('email')
        company = request.form.get('company')
        message = request.form.get('message')

        success, result = notion.add_contact(name, email, message, company)

        if success:
            # Send email notification
            try:
                msg = Message(
                    'Nuovo messaggio dal form di contatto',
                    recipients=[app.config['MAIL_RECIPIENT']],
                    body=f'''Nuovo messaggio ricevuto:
                    
Da: {name} ({email})
Azienda: {company}
Messaggio:
{message}'''
                )
                mail.send(msg)
            except Exception as e:
                print(f"Errore nell'invio dell'email: {str(e)}")

            flash('Grazie per avermi contattato! Ti risponderò il prima possibile.', 'success')
        else:
            error_msg = f'Errore: {result}' if result else 'Si è verificato un errore durante l\'invio del messaggio.'
            flash(error_msg, 'error')
            print(f"Errore dettagliato: {result}")

        return redirect(url_for('contact'))

    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)