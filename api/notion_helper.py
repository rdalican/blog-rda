import os
from notion_client import Client
from datetime import datetime
import markdown2
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.environ.get("NOTION_TOKEN"))
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

def get_blog_posts():
    """
    Retrieve all published blog posts from Notion database
    """
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            filter={
                "property": "Stato",
                "select": {
                    "equals": "Pubblicato"
                }
            },
            sorts=[{
                "property": "Data",
                "direction": "descending"
            }]
        )
        
        posts = []
        for page in response["results"]:
            properties = page["properties"]
            
            # Extract post data using the correct column names
            title = properties["Name"]["title"][0]["text"]["content"] if properties["Name"]["title"] else "Senza titolo"
            date = properties["Data"]["date"]["start"] if properties["Data"]["date"] else datetime.now().isoformat()
            content = properties["Messaggio"]["rich_text"][0]["text"]["content"] if properties["Messaggio"]["rich_text"] else ""
            post_id = properties["Post ID"]["rich_text"][0]["text"]["content"] if properties["Post ID"]["rich_text"] else ""
            email = properties["Email"]["email"] if properties["Email"]["email"] else ""
            stato = properties["Stato"]["select"]["name"] if properties["Stato"]["select"] else ""
            
            # Convert content from Markdown to HTML
            html_content = markdown2.markdown(content)
            
            posts.append({
                "id": page["id"],
                "title": title,
                "date": date,
                "content": html_content,
                "post_id": post_id,
                "email": email,
                "stato": stato
            })
            
        return posts
    except Exception as e:
        print(f"Error fetching blog posts: {str(e)}")
        return []

def get_post_by_id(post_id):
    """
    Retrieve a specific published blog post by its Post ID
    """
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            filter={
                "and": [
                    {
                        "property": "Post ID",
                        "rich_text": {
                            "equals": post_id
                        }
                    },
                    {
                        "property": "Stato",
                        "select": {
                            "equals": "Pubblicato"
                        }
                    }
                ]
            }
        )
        
        if not response["results"]:
            return None
            
        page = response["results"][0]
        properties = page["properties"]
        
        title = properties["Name"]["title"][0]["text"]["content"] if properties["Name"]["title"] else "Senza titolo"
        date = properties["Data"]["date"]["start"] if properties["Data"]["date"] else datetime.now().isoformat()
        content = properties["Messaggio"]["rich_text"][0]["text"]["content"] if properties["Messaggio"]["rich_text"] else ""
        email = properties["Email"]["email"] if properties["Email"]["email"] else ""
        stato = properties["Stato"]["select"]["name"] if properties["Stato"]["select"] else ""
        
        # Convert content from Markdown to HTML
        html_content = markdown2.markdown(content)
        
        return {
            "id": page["id"],
            "title": title,
            "date": date,
            "content": html_content,
            "post_id": post_id,
            "email": email,
            "stato": stato
        }
    except Exception as e:
        print(f"Error fetching blog post: {str(e)}")
        return None