import os
from notion_client import Client
from datetime import datetime
from dotenv import load_dotenv
import uuid

load_dotenv()

# Initialize the Notion client
notion = Client(auth=os.environ.get("NOTION_TOKEN"))
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")

# Sample blog posts
sample_posts = [
    {
        "title": "Benvenuti nel Blog RdA",
        "content": """
# Benvenuti nel mio blog!

Sono lieto di darvi il benvenuto in questo spazio dedicato alla condivisione di idee, riflessioni e esperienze.

In questo blog tratteremo diversi argomenti, tra cui:
- Riflessioni personali
- Esperienze di vita
- Temi di attualità
- E molto altro ancora...

Vi invito a seguire il blog e a partecipare attivamente attraverso i commenti.

A presto!
        """,
        "stato": "pubblicato"
    },
    {
        "title": "L'importanza della condivisione",
        "content": """
# L'importanza della condivisione

La condivisione è uno dei valori più importanti nella nostra società. Attraverso la condivisione di:
- Esperienze
- Conoscenze
- Emozioni
- Riflessioni

possiamo crescere insieme e creare connessioni significative.

Questo blog nasce proprio con questo spirito: creare uno spazio di condivisione e dialogo.
        """,
        "stato": "pubblicato"
    },
    {
        "title": "Riflessioni sul futuro",
        "content": """
# Riflessioni sul futuro

Il futuro è un tema che ci coinvolge tutti. In questo articolo, esploreremo:

## Le sfide che ci attendono
- Cambiamenti sociali
- Evoluzione tecnologica
- Sostenibilità ambientale

## Le opportunità da cogliere
- Innovazione
- Collaborazione
- Crescita personale

Insieme possiamo costruire un futuro migliore.
        """,
        "stato": "pubblicato"
    }
]

def create_post(post_data):
    """Create a new post in the Notion database"""
    try:
        post_id = str(uuid.uuid4())[:8]  # Generate a short unique ID
        
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Name": {
                    "title": [{"text": {"content": post_data["title"]}}]
                },
                "Messaggio": {
                    "rich_text": [{"text": {"content": post_data["content"]}}]
                },
                "Post ID": {
                    "rich_text": [{"text": {"content": post_id}}]
                },
                "Data": {
                    "date": {"start": datetime.now().isoformat()}
                },
                "Stato": {
                    "select": {"name": post_data["stato"]}
                },
                "Email": {
                    "email": "blog@example.com"
                }
            }
        )
        print(f"Created post: {post_data['title']} with ID: {post_id}")
        return True
    except Exception as e:
        print(f"Error creating post: {str(e)}")
        return False

def main():
    if not os.environ.get("NOTION_TOKEN") or not os.environ.get("NOTION_DATABASE_ID"):
        print("Error: NOTION_TOKEN and NOTION_DATABASE_ID must be set in environment variables")
        return
        
    print("Creating sample blog posts...")
    for post in sample_posts:
        if create_post(post):
            print(f"Successfully created: {post['title']}")
        else:
            print(f"Failed to create: {post['title']}")
    print("Done!")

if __name__ == "__main__":
    main() 