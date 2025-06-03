from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
from notion_manager import NotionManager
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('Config_Email.env')

app = Flask(__name__)
# Modifica per Vercel: usa un database in memoria per l'ambiente di produzione
if os.environ.get('VERCEL_ENV') == 'production':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Email configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_RECIPIENT'] = os.environ.get('MAIL_RECIPIENT')

db = SQLAlchemy(app)
mail = Mail(app)

try:
    notion = NotionManager()
except Exception as e:
    print(f"Errore durante l'inizializzazione di Notion: {str(e)}")
    notion = None

# Inizializza il database e aggiungi alcuni post di esempio se siamo in produzione
def init_db():
    with app.app_context():
        db.create_all()
        # Se siamo su Vercel e il database è vuoto, aggiungi alcuni post di esempio
        if os.environ.get('VERCEL_ENV') == 'production' and not Post.query.first():
            sample_posts = [
                {
                    'title': 'Benvenuto nel Blog',
                    'content': 'Questo è un post di esempio creato automaticamente.'
                },
                {
                    'title': 'Come Funziona',
                    'content': 'Questo blog usa Flask, SQLite e Notion per gestire i commenti.'
                }
            ]
            for post_data in sample_posts:
                post = Post(title=post_data['title'], content=post_data['content'])
                db.session.add(post)
            db.session.commit()

# Inizializza il database
init_db()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.template_filter('regex_replace')
def regex_replace(s, find, replace=''):
    """A non-optimal implementation of a regex filter"""
    return re.sub(find, replace, s)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    success, comments = notion.get_comments_for_post(str(post_id))
    return render_template('post.html', post=post, comments=comments if success else [])

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    if notion is None:
        flash('Configurazione Notion non disponibile. Contatta l\'amministratore.', 'error')
        return redirect(url_for('post', post_id=post_id))

    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Get the post title
    post = Post.query.get_or_404(post_id)
    post_title = post.title

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
    with app.app_context():
        db.create_all()
    app.run(debug=True)