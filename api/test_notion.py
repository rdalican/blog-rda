import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

def test_notion_connection():
    token = os.environ.get("NOTION_TOKEN")
    database_id = os.environ.get("NOTION_DATABASE_ID")
    
    print(f"Testing Notion connection...")
    print(f"Token available: {'Yes' if token else 'No'}")
    print(f"Database ID available: {'Yes' if database_id else 'No'}")
    
    try:
        notion = Client(auth=token)
        
        # Try to access the database
        response = notion.databases.retrieve(database_id=database_id)
        print("\nDatabase connection successful!")
        print(f"Database title: {response['title'][0]['plain_text']}")
        print(f"Database ID: {response['id']}")
        
        # List the properties
        print("\nDatabase properties:")
        for prop_name, prop_data in response['properties'].items():
            print(f"- {prop_name} ({prop_data['type']})")
            
    except Exception as e:
        print(f"\nError connecting to Notion: {str(e)}")

if __name__ == "__main__":
    test_notion_connection() 