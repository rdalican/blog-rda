import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime

class NotionManager:
    def __init__(self):
        # Debug info per l'ambiente
        print("=== Debug Informazioni Notion ===")
        print(f"Directory corrente: {os.getcwd()}")
        print(f"File di configurazione esiste: {os.path.exists('Config_Notion.env')}")
        
        # Caricamento configurazione
        load_dotenv('Config_Notion.env')
        self.token = os.getenv('NOTION_TOKEN')
        self.contacts_db_id = os.getenv('NOTION_DATABASE_ID')
        self.comments_db_id = "2062c37023cf80dba102d26f3a01173c"
        
        # Debug info per le credenziali
        print(f"Token Notion trovato: {'Sì' if self.token else 'No'}")
        print(f"Token Notion lunghezza: {len(self.token) if self.token else 0}")
        print(f"Database Contatti ID: {self.contacts_db_id}")
        print(f"Database Commenti ID: {self.comments_db_id}")
        
        if not self.token or not self.contacts_db_id:
            raise ValueError("Token Notion o Database ID mancanti nel file Config_Notion.env")
            
        try:
            print("\nTentativo di connessione a Notion...")
            self.notion = Client(auth=self.token)
            
            # Test della connessione ai database
            print(f"Verifica accesso al database contatti: {self.contacts_db_id}")
            contacts_db = self.notion.databases.retrieve(self.contacts_db_id)
            print("✅ Database contatti trovato!")
            
            print(f"Verifica accesso al database commenti: {self.comments_db_id}")
            comments_db = self.notion.databases.retrieve(self.comments_db_id)
            print("✅ Database commenti trovato!")
            
        except Exception as e:
            print(f"\n❌ Errore di connessione a Notion: {str(e)}")
            raise

    def add_contact(self, name, email, message, company=None):
        """
        Aggiunge un nuovo contatto al database Notion
        """
        try:
            new_page = {
                "Name": {"title": [{"text": {"content": name}}]},
                "Email": {"email": email},
                "Messaggio": {"rich_text": [{"text": {"content": message}}]},
                "Stato": {"select": {"name": "Nuovo"}},
            }
            
            if company:
                new_page["Azienda"] = {"rich_text": [{"text": {"content": company}}]}

            print(f"Tentativo di aggiunta contatto al database: {self.contacts_db_id}")
            response = self.notion.pages.create(
                parent={"database_id": self.contacts_db_id},
                properties=new_page
            )
            print(f"✅ Contatto aggiunto con successo: {name}")
            return True, response
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Errore durante l'aggiunta del contatto: {error_msg}")
            return False, error_msg

    def add_comment(self, name, email, message, post_id):
        """
        Aggiunge un nuovo commento al database dei commenti
        """
        try:
            new_comment = {
                "Name": {"title": [{"text": {"content": name}}]},
                "Email": {"email": email},
                "Messaggio": {"rich_text": [{"text": {"content": message}}]},
                "Post ID": {"rich_text": [{"text": {"content": post_id}}]},
                "Data": {"date": {"start": datetime.utcnow().isoformat()}},
                "Stato": {"select": {"name": "Nuovo"}}
            }

            print(f"Tentativo di aggiunta commento per il post {post_id}")
            response = self.notion.pages.create(
                parent={"database_id": self.comments_db_id},
                properties=new_comment
            )
            print(f"✅ Commento aggiunto con successo da: {name}")
            return True, response
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Errore durante l'aggiunta del commento: {error_msg}")
            return False, error_msg

    def get_comments_for_post(self, post_id):
        """
        Recupera tutti i commenti per un post specifico
        """
        try:
            print(f"Recupero commenti per il post: {post_id}")
            response = self.notion.databases.query(
                database_id=self.comments_db_id,
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
                                "equals": "Approvato"
                            }
                        }
                    ]
                },
                sorts=[
                    {
                        "property": "Data",
                        "direction": "descending"
                    }
                ]
            )
            
            comments = []
            for page in response['results']:
                props = page['properties']
                comment = {
                    'name': props['Name']['title'][0]['text']['content'] if props['Name']['title'] else 'Anonimo',
                    'message': props['Messaggio']['rich_text'][0]['text']['content'] if props['Messaggio']['rich_text'] else '',
                    'date': datetime.fromisoformat(props['Data']['date']['start'].replace('Z', '+00:00'))
                }
                comments.append(comment)
                
            print(f"✅ Recuperati {len(comments)} commenti")
            return True, comments
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Errore durante il recupero dei commenti: {error_msg}")
            return False, error_msg

    def get_contacts(self):
        """
        Recupera tutti i contatti dal database
        """
        try:
            print(f"Tentativo di recupero contatti dal database: {self.contacts_db_id}")
            response = self.notion.databases.query(
                database_id=self.contacts_db_id,
                sorts=[{"property": "Name", "direction": "ascending"}]
            )
            print(f"✅ Recuperati {len(response['results'])} contatti")
            return True, response['results']
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Errore durante il recupero dei contatti: {error_msg}")
            return False, error_msg 