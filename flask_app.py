import sys

# Add your project's directory to the Python path.
# This is the directory where your blog_app.py file is located.
path = '/home/rdalican/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

# Import the Flask app instance
from blog_app import app as application