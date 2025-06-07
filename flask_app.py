from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Questa funzione gestisce la rotta principale ('/') del sito.
    Utilizza render_template per mostrare il file 'index.html'
    che si trova nella cartella 'templates'.
    """
    return render_template('index.html')

@app.route('/about')
def about():
    """
    Questa funzione gestisce la rotta '/about'.
    Utilizza render_template per mostrare il file 'about.html'.
    """
    return render_template('about.html')

@app.route('/blog')
def blog():
    """
    Questa funzione gestisce la rotta '/blog'.
    Utilizza render_template per mostrare il file 'blog.html'.
    """
    return render_template('blog.html')

# Questo blocco permette di eseguire l'app localmente per test
# PythonAnywhere non lo userà direttamente, ma è buona norma includerlo.
if __name__ == '__main__':
    app.run(debug=True)
