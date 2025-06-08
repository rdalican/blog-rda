import requests
import os
import time
import re

# --- Configuration ---
PYTHONANYWHERE_USERNAME = "rdalican"
PYTHONANYWHERE_TOKEN = "b6b8f41c8765e0147529d3694e3208e08a3a10a6"
DOMAIN_NAME = "rdalican.pythonanywhere.com"
PROJECT_PATH = os.path.abspath(".")
REMOTE_PROJECT_NAME = "Blopg_RdA"
FLASK_APP_FILE = "flask_app.py"
PYTHON_VERSION = "python3.9"

# --- API Endpoints ---
BASE_URL = "https://www.pythonanywhere.com/api/v0/user/{username}/"
WEBAPP_URL = BASE_URL + "webapps/{domain_name}/"
RELOAD_URL = WEBAPP_URL + "reload/"
STATIC_FILES_URL = BASE_URL + "files/path/home/{username}/{project_name}/"

def get_headers():
    return {"Authorization": f"Token {PYTHONANYWHERE_TOKEN}"}

def delete_existing_webapp():
    """Deletes the existing web app."""
    print(f"Deleting web app: {DOMAIN_NAME}...")
    url = WEBAPP_URL.format(username=PYTHONANYWHERE_USERNAME, domain_name=DOMAIN_NAME)
    response = requests.delete(url, headers=get_headers())
    if response.status_code == 204:
        print("Web app deleted successfully.")
    elif response.status_code == 404:
        print("Web app not found, skipping deletion.")
    else:
        print(f"Error deleting web app: {response.status_code} - {response.text}")
        exit(1)

def create_new_webapp():
    """Creates a new web app."""
    print(f"Creating new web app: {DOMAIN_NAME}...")
    url = BASE_URL.format(username=PYTHONANYWHERE_USERNAME) + "webapps/"
    data = {
        "domain_name": DOMAIN_NAME,
        "python_version": PYTHON_VERSION,
    }
    response = requests.post(url, headers=get_headers(), data=data)
    if response.status_code == 201:
        print("Web app created successfully.")
    else:
        print(f"Error creating web app: {response.status_code} - {response.text}")
        exit(1)

def upload_project_files():
    """Uploads the project files to PythonAnywhere."""
    print("Uploading project files...")
    project_base_remote = f"/home/{PYTHONANYWHERE_USERNAME}/{REMOTE_PROJECT_NAME}"

    # Exclude files and directories that shouldn't be uploaded
    exclude_files = ['deploy_to_pythonanywhere.py']
    exclude_dirs = ['.git', 'venv', '__pycache__', 'instance']

    for root, dirs, files in os.walk(PROJECT_PATH, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            if file in exclude_files:
                continue

            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, PROJECT_PATH)
            remote_file_path = f"{project_base_remote}/{relative_path.replace(os.sep, '/')}"
            url = f"https://www.pythonanywhere.com/api/v0/user/{PYTHONANYWHERE_USERNAME}/files/path{remote_file_path}"

            while True:
                with open(local_path, 'rb') as f:
                    try:
                        response = requests.post(url, headers=get_headers(), files={'content': f}, timeout=60)
                    except requests.exceptions.RequestException as e:
                        print(f"  - Network error uploading {relative_path}: {e}")
                        time.sleep(10) # Wait before retrying on network error
                        continue

                if response.status_code in [200, 201]:
                    status = "Overwrote" if response.status_code == 200 else "Uploaded"
                    print(f"  - {status} {relative_path}")
                    time.sleep(0.2)  # Small delay to be nice to the API
                    break
                elif response.status_code == 429:
                    print(f"  - Throttled. Waiting and retrying {relative_path}...")
                    time.sleep(10)  # Wait for 10 seconds if throttled
                else:
                    print(f"  - Error uploading {relative_path}: {response.status_code} - {response.text}")
                    break


def configure_wsgi_file():
    """Configures the WSGI file for the Flask app."""
    print("Configuring WSGI file...")
    project_home = f'/home/{PYTHONANYWHERE_USERNAME}/{REMOTE_PROJECT_NAME}'
    wsgi_content = f"""
import sys
path = '{project_home}'
if path not in sys.path:
    sys.path.insert(0, path)
from {FLASK_APP_FILE.replace('.py', '')} import app as application
"""
    # The path to the WSGI file for your web app
    wsgi_path = f"/var/www/{DOMAIN_NAME.replace('.', '_')}_wsgi.py"
    url = f"https://www.pythonanywhere.com/api/v0/user/{PYTHONANYWHERE_USERNAME}/files/path{wsgi_path}"

    response = requests.post(url, headers=get_headers(), files={'content': wsgi_content})

    if response.status_code in [200, 201]:
        print("WSGI file configured successfully.")
    else:
        print(f"Error configuring WSGI file: {response.status_code} - {response.text}")
        exit(1)


def install_dependencies():
    """Installs the required dependencies using pip."""
    print("Installing dependencies from requirements.txt...")
    requirements_path = f"/home/{PYTHONANYWHERE_USERNAME}/{REMOTE_PROJECT_NAME}/requirements.txt"
    command = f"pip3.9 install --user -r {requirements_path}"
    url = BASE_URL.format(username=PYTHONANYWHERE_USERNAME) + "consoles/"
    response = requests.post(url, headers=get_headers(), data={"executable": "bash", "arguments": f"-c '{command}'"})

    if response.status_code == 201:
        print("  - Console created to install dependencies.")
    elif "Console limit reached" in response.text:
        print("  - Console limit reached. Cannot install dependencies automatically.")
        print("  - Please run the following command in a PythonAnywhere bash console:")
        print(f"  - {command}")
    else:
        print(f"  - Could not create console for dependency installation: {response.status_code} - {response.text}")


def reload_webapp():
    """Reloads the web app to apply changes."""
    print("Reloading web app...")
    url = WEBAPP_URL.format(username=PYTHONANYWHERE_USERNAME, domain_name=DOMAIN_NAME) + "reload/"
    response = requests.post(url, headers=get_headers())
    if response.status_code == 200:
        print("Web app reloaded successfully.")
    else:
        print(f"Error reloading web app: {response.status_code} - {response.text}")
        print("Please try reloading the web app manually from your PythonAnywhere dashboard.")
        exit(1)

if __name__ == "__main__":
    # delete_existing_webapp()
    # create_new_webapp()
    upload_project_files()
    configure_wsgi_file()
    install_dependencies()
    print("\nFile upload and configuration complete.")
    print("Attempting to reload web app...")
    reload_webapp()
    print("\nDeployment to PythonAnywhere completed successfully!")
    print(f"Your site is live at: http://{DOMAIN_NAME}")