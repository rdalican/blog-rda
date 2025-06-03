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
    Retrieve all blog posts from Notion database
    """
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            sorts=[{
                "property": "Date",
                "direction": "descending"
            }]
        )
        
        posts = []
        for page in response["results"]:
            properties = page["properties"]
            
            # Extract post data
            title = properties["Title"]["title"][0]["text"]["content"] if properties["Title"]["title"] else "Untitled"
            date = properties["Date"]["date"]["start"] if properties["Date"]["date"] else datetime.now().isoformat()
            content = properties["Content"]["rich_text"][0]["text"]["content"] if properties["Content"]["rich_text"] else ""
            slug = properties["Slug"]["rich_text"][0]["text"]["content"] if properties["Slug"]["rich_text"] else ""
            
            # Convert content from Markdown to HTML
            html_content = markdown2.markdown(content)
            
            posts.append({
                "id": page["id"],
                "title": title,
                "date": date,
                "content": html_content,
                "slug": slug
            })
            
        return posts
    except Exception as e:
        print(f"Error fetching blog posts: {str(e)}")
        return []

def get_post_by_slug(slug):
    """
    Retrieve a specific blog post by its slug
    """
    try:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            filter={
                "property": "Slug",
                "rich_text": {
                    "equals": slug
                }
            }
        )
        
        if not response["results"]:
            return None
            
        page = response["results"][0]
        properties = page["properties"]
        
        title = properties["Title"]["title"][0]["text"]["content"] if properties["Title"]["title"] else "Untitled"
        date = properties["Date"]["date"]["start"] if properties["Date"]["date"] else datetime.now().isoformat()
        content = properties["Content"]["rich_text"][0]["text"]["content"] if properties["Content"]["rich_text"] else ""
        
        # Convert content from Markdown to HTML
        html_content = markdown2.markdown(content)
        
        return {
            "id": page["id"],
            "title": title,
            "date": date,
            "content": html_content,
            "slug": slug
        }
    except Exception as e:
        print(f"Error fetching blog post: {str(e)}")
        return None 