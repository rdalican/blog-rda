import os
import sys
from dotenv import load_dotenv
from notion_manager import NotionManager
from bs4 import BeautifulSoup

# --- Configuration ---
# The base URL for your website, used to construct full image paths.
# This should be the URL where your static files are served.
BASE_URL = "https://rdalican.pythonanywhere.com"

def add_blog_post(file_path):
    """
    Reads an HTML file, processes its content to fix image paths,
    and adds it as a new post to the Notion database.
    """
    print(f"--- Starting to process post from: {file_path} ---")

    # 1. Check if the file exists
    if not os.path.exists(file_path):
        print(f"[ERROR] The file '{file_path}' was not found.")
        return

    # 2. Read the HTML content from the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"[ERROR] Could not read the file: {e}")
        return

    # 3. Parse the HTML and extract the title
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract title from the <title> tag
        post_title = soup.title.string if soup.title else "Senza titolo"
        print(f"Extracted Post Title: '{post_title}'")

        # --- Process Image Paths ---
        images = soup.find_all('img')
        if images:
            print(f"Found {len(images)} image(s). Processing paths...")
            for img in images:
                src = img.get('src')
                if src and not src.startswith(('http://', 'https://')):
                    # Prepend the base URL to relative paths
                    absolute_src = f"{BASE_URL}/static/{src.lstrip('/')}"
                    img['src'] = absolute_src
                    print(f"  - Converted '{src}' to '{absolute_src}'")
            
            # Get the updated HTML content
            processed_html = str(soup)
        else:
            print("No images found in the post.")
            processed_html = html_content

    except Exception as e:
        print(f"[ERROR] Failed to parse or process the HTML: {e}")
        return

    # 4. Connect to Notion and add the post
    try:
        print("\nConnecting to Notion...")
        load_dotenv(dotenv_path='Config_Notion.env')
        notion = NotionManager()

        # Determine the next Post ID
        success, posts = notion.get_blog_posts()
        if not success:
            print("[WARNING] Could not retrieve existing posts to determine the next ID. Defaulting to a random ID.")
            next_post_id = str(len(posts) + 1) # Fallback
        else:
            next_post_id = str(len(posts) + 1)
        
        print(f"Assigning new Post ID: {next_post_id}")

        print("Creating new post in Notion...")
        success, result = notion.add_blog_post(
            title=post_title,
            html_content=processed_html,
            status="Pubblicato",
            post_id_slug=next_post_id
        )

        if success:
            print("\n--- ✅ SUCCESS! ---")
            print(f"The post '{post_title}' has been successfully added to your blog.")
            print(f"You can view it at: {BASE_URL}/post/{next_post_id}")
        else:
            print(f"\n--- ❌ FAILED ---")
            print(f"Failed to create the post in Notion: {result}")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] An unexpected error occurred while connecting to Notion or adding the post: {e}")

if __name__ == "__main__":
    # Check if a filename was provided as a command-line argument
    if len(sys.argv) < 2:
        print("--- Simple Blog Post Uploader ---")
        print("This script reads an HTML file and adds it as a new post to your blog.")
        print("\nUsage: python add_blog_post.py <path_to_your_html_file>")
        print("\nExample: python add_blog_post.py \"My New Post.html\"")
    else:
        # The first argument is the script name, the second is the file path
        html_file_path = sys.argv[1]
        add_blog_post(html_file_path)