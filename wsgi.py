# +++++++++++ FLASK +++++++++++
# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The important part is "from blog_app import app as application"

import sys
from dotenv import load_dotenv
import os

# add your project directory to the sys.path
project_home = u'/home/rdalican/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# load environment variables from .env files
load_dotenv(os.path.join(project_home, 'Config_Email.env'))
load_dotenv(os.path.join(project_home, 'Config_Notion.env'))

# import flask app but need to call it "application" for WSGI to work
from blog_app import app as application