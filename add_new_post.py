from notion_manager import NotionManager
from datetime import datetime

def main():
    """Reads the post content from a file and adds it to the Notion database."""
    
    post_title = "Il Valore in Evoluzione: Navigare il Futuro del Lavoro nell'Era dell'IA"
    
    try:
        with open('post1.txt', 'r', encoding='utf-8') as f:
            post_content = f.read()
    except FileNotFoundError:
        print("Error: post1.txt not found. Please make sure the file exists in the same directory.")
        return

    print("Connecting to Notion...")
    notion = NotionManager()
    
    # Define the post properties
    properties = {
        "Name": {"title": [{"text": {"content": post_title}}]},
        "Messaggio": {"rich_text": [{"text": {"content": post_content}}]},
        "Post ID": {"rich_text": [{"text": {"content": "1"}}]},
        "Stato": {"select": {"name": "Pubblicato"}},
        "Data": {"date": {"start": datetime.now().isoformat()}}
    }
    
    print("Creating new post in Notion...")
    success, result = notion.add_blog_post(
        title=post_title,
        html_content=post_content,
        status="Pubblicato",
        post_id_slug="1"
    )
    
    if success:
        print("Post created successfully!")
    else:
        print(f"Failed to create post: {result}")

if __name__ == "__main__":
    main()