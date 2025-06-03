import os
from notion_client import Client
from dotenv import load_dotenv

class NotionManager:
    def __init__(self):
        # Load environment variables
        self.token = os.environ.get('NOTION_TOKEN')
        self.database_id_contacts = os.environ.get('NOTION_DATABASE_ID_CONTACTS')
        self.database_id_comments = os.environ.get('NOTION_DATABASE_ID_COMMENTS')
        
        if not all([self.token, self.database_id_contacts, self.database_id_comments]):
            raise ValueError("Missing required Notion configuration")

        self.notion = Client(auth=self.token)
        
        # Verify database access
        try:
            self.notion.databases.retrieve(self.database_id_contacts)
            print("✅ Database contatti trovato!")
        except Exception as e:
            print(f"❌ Errore nell'accesso al database contatti: {str(e)}")
            raise

        try:
            self.notion.databases.retrieve(self.database_id_comments)
            print("✅ Database commenti trovato!")
        except Exception as e:
            print(f"❌ Errore nell'accesso al database commenti: {str(e)}")
            raise

    def add_contact(self, name, email, message, company=None):
        try:
            new_page = {
                "Nome": {"title": [{"text": {"content": name}}]},
                "Email": {"email": email},
                "Messaggio": {"rich_text": [{"text": {"content": message}}]},
            }
            
            if company:
                new_page["Azienda"] = {"rich_text": [{"text": {"content": company}}]}

            response = self.notion.pages.create(
                parent={"database_id": self.database_id_contacts},
                properties=new_page
            )
            print(f"✅ Contatto aggiunto con successo: {name}")
            return True, None
        except Exception as e:
            print(f"❌ Errore nell'aggiunta del contatto: {str(e)}")
            return False, str(e)

    def add_comment(self, name, email, message, post_id):
        try:
            new_page = {
                "Nome": {"title": [{"text": {"content": name}}]},
                "Email": {"email": email},
                "Commento": {"rich_text": [{"text": {"content": message}}]},
                "Post ID": {"rich_text": [{"text": {"content": post_id}}]},
                "Approvato": {"checkbox": False}
            }

            response = self.notion.pages.create(
                parent={"database_id": self.database_id_comments},
                properties=new_page
            )
            print(f"✅ Commento aggiunto con successo da: {name}")
            return True, None
        except Exception as e:
            print(f"❌ Errore nell'aggiunta del commento: {str(e)}")
            return False, str(e)

    def get_comments_for_post(self, post_id):
        try:
            print(f"Recupero commenti per il post: {post_id}")
            response = self.notion.databases.query(
                database_id=self.database_id_comments,
                filter={
                    "and": [
                        {
                            "property": "Post ID",
                            "rich_text": {
                                "equals": post_id
                            }
                        },
                        {
                            "property": "Approvato",
                            "checkbox": {
                                "equals": True
                            }
                        }
                    ]
                }
            )
            
            comments = []
            for page in response["results"]:
                props = page["properties"]
                comment = {
                    "name": props["Nome"]["title"][0]["text"]["content"] if props["Nome"]["title"] else "Anonimo",
                    "message": props["Commento"]["rich_text"][0]["text"]["content"] if props["Commento"]["rich_text"] else "",
                    "date": page["created_time"]
                }
                comments.append(comment)
            
            print(f"✅ Recuperati {len(comments)} commenti")
            return True, comments
        except Exception as e:
            print(f"❌ Errore nel recupero dei commenti: {str(e)}")
            return False, [] 