import os
import requests

# --- PythonAnywhere Configuration ---
PYTHONANYWHERE_API_TOKEN = "b6b8f41c8765e0147529d3694e3208e08a3a10a6"
PYTHONANYWHERE_USERNAME = "rdalican"
PYTHONANYWHERE_DOMAIN = f"{PYTHONANYWHERE_USERNAME}.pythonanywhere.com"

# --- Project Configuration ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_NAME = "flask_blog_venv"
VENV_PATH = f"/home/{PYTHONANYWHERE_USERNAME}/.virtualenvs/{VENV_NAME}"
WSGI_FILE_PATH = f"/var/www/{PYTHONANYWHERE_USERNAME}_pythonanywhere_com_wsgi.py"

# --- API Endpoints ---
RELOAD_WEB_APP_URL = f"https://www.pythonanywhere.com/api/v0/user/{PYTHONANYWHERE_USERNAME}/webapps/{PYTHONANYWHERE_DOMAIN}/reload/"

def upload_file(file_path, remote_path):
    """Uploads a file to PythonAnywhere."""
    url = f"https://www.pythonanywhere.com/api/v0/user/{PYTHONANYWHERE_USERNAME}/files/path{remote_path}"
    headers = {"Authorization": f"Token {PYTHONANYWHERE_API_TOKEN}"}
    with open(file_path, 'rb') as f:
        files = {'content': f}
        response = requests.post(url, headers=headers, files=files)
    if response.status_code in [200, 201]:
        print(f"Successfully uploaded {os.path.basename(file_path)} to {remote_path}")
    else:
        print(f"Failed to upload {os.path.basename(file_path)}. Status: {response.status_code}, Response: {response.text}")

def main():
    """Main deployment script."""
    print("--- Starting Deployment to PythonAnywhere ---")

    # --- List of files to upload ---
    files_to_upload = [
        "blog_app.py",
        "notion_manager.py",
        "requirements.txt",
        "flask_app.py",
        "Config_Email.env",
        "Config_Notion.env"
    ]

    # --- Upload project files ---
    for file in files_to_upload:
        upload_file(os.path.join(PROJECT_DIR, file), f"/home/{PYTHONANYWHERE_USERNAME}/mysite/{file}")

    # --- Upload WSGI file ---
    print("--- Uploading WSGI configuration ---")
    upload_file(os.path.join(PROJECT_DIR, "wsgi.py"), WSGI_FILE_PATH)

    # --- Upload templates ---
    templates_dir = os.path.join(PROJECT_DIR, "templates")
    for template in os.listdir(templates_dir):
        upload_file(os.path.join(templates_dir, template), f"/home/{PYTHONANYWHERE_USERNAME}/mysite/templates/{template}")

    # --- Upload static files ---
    static_dir = os.path.join(PROJECT_DIR, "static")
    for root, _, files in os.walk(static_dir):
        for file in files:
            local_path = os.path.join(root, file)
            remote_path = os.path.join(f"/home/{PYTHONANYWHERE_USERNAME}/mysite", os.path.relpath(local_path, PROJECT_DIR)).replace("\\", "/")
            upload_file(local_path, remote_path)

    # --- Reload the web app ---
    headers = {"Authorization": f"Token {PYTHONANYWHERE_API_TOKEN}"}
    response = requests.post(RELOAD_WEB_APP_URL, headers=headers)
    if response.status_code == 200:
        print("Web app reloaded successfully.")
    else:
        print(f"Failed to reload web app. Status: {response.status_code}, Response: {response.text}")

    print("--- Deployment Finished ---")

if __name__ == "__main__":
    main()