# Flask Blog with Notion DB Deployment to PythonAnywhere

This document outlines the steps to deploy the Flask blog application to PythonAnywhere.

## Prerequisites

- A PythonAnywhere account.
- Your PythonAnywhere API token.
- Your Notion API token and database IDs.
- Your email provider credentials.

## Deployment Steps

1.  **Set API Token:**
    - Open `deploy_to_pythonanywhere.py`.
    - Replace `YOUR_PYTHONANYWHERE_API_TOKEN` with your actual PythonAnywhere API token.

2.  **Configure Environment Variables:**
    - Ensure `Config_Email.env` and `Config_Notion.env` have the correct production values.

3.  **Run Deployment Script:**
    - Execute the deployment script from your local machine:
      ```bash
      python deploy_to_pythonanywhere.py
      ```

4.  **PythonAnywhere Console Setup:**
    - Log in to your PythonAnywhere account and open a **Bash Console**.
    - Create a virtual environment (replace with your desired Python version):
      ```bash
      mkvirtualenv --python=python3.9 flask_blog_venv
      ```
    - Navigate to your project directory:
      ```bash
      cd ~/mysite
      ```
    - Install the required packages:
      ```bash
      pip install -r requirements.txt
      ```

5.  **Configure PythonAnywhere Web App:**
    - Go to the **Web** tab in your PythonAnywhere dashboard.
    - **Add a new web app**:
        - Select **Manual configuration**.
        - Select **Python 3.9** (or the version you used for the virtualenv).
    - **Web App Configuration**:
        - **Source code**: `/home/rdalican/mysite`
        - **Virtualenv**: `/home/rdalican/.virtualenvs/flask_blog_venv`
    - **WSGI Configuration**:
        - Click on the link to the WSGI configuration file (e.g., `/var/www/rdalican_pythonanywhere_com_wsgi.py`).
        - Replace the entire content of this file with the content from your local `flask_app.py`.
    - **Reload Web App**:
        - Click the "Reload" button on the Web tab.

Your application should now be live at `http://rdalican.pythonanywhere.com`.