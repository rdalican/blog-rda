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

# Questo blocco permette di eseguire l'app localmente per test
# PythonAnywhere non lo userà direttamente, ma è buona norma includerlo.
if __name__ == '__main__':
    app.run(debug=True)
