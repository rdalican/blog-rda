import os
from notion_client import Client
from dotenv import load_dotenv
from datetime import datetime, timezone
import markdown2

class NotionManager:
    def __init__(self):
        # Caricamento configurazione
        # Le variabili d'ambiente vengono caricate dal file blog_app.py
        self.token = os.getenv('NOTION_TOKEN')
        self.contacts_db_id = os.getenv('NOTION_CONTACTS_DB_ID')
        self.comments_db_id = os.getenv('NOTION_COMMENTS_DB_ID')
        
        # Carica l'ID del database dei post o usa un fallback
        self.posts_db_id_env = os.getenv('NOTION_POSTS_DB_ID')
        if self.posts_db_id_env:
            self.posts_db_id = self.posts_db_id_env
            print(f"ID Database Post da .env: {self.posts_db_id}")
        else:
            self.posts_db_id = self.contacts_db_id  # Fallback al database dei contatti
            print(f"ATTENZIONE: NOTION_POSTS_DB_ID non trovato in Config_Notion.env. Uso {self.contacts_db_id} come fallback per i post.")
            print("Si consiglia di creare un database dedicato per i post e configurare NOTION_POSTS_DB_ID.")

        # Debug info per le credenziali
        print(f"Token Notion trovato: {'Sì' if self.token else 'No'}")
        print(f"Token Notion lunghezza: {len(self.token) if self.token else 0}")
        print(f"Database Contatti ID: {self.contacts_db_id}")
        print(f"Database Commenti ID: {self.comments_db_id}")
        print(f"Database Posts ID: {self.posts_db_id}")
        
        if not self.token or not self.contacts_db_id:
            raise ValueError("Token Notion o Database ID mancanti nel file Config_Notion.env")
            
        try:
            print("\nTentativo di connessione a Notion...")
            self.notion = Client(auth=self.token)
            
            # Test della connessione ai database
            print(f"Verifica accesso al database contatti: {self.contacts_db_id}")
            contacts_db = self.notion.databases.retrieve(self.contacts_db_id)
            print("[OK] Database contatti trovato!")
            
            print(f"Verifica accesso al database commenti: {self.comments_db_id}")
            comments_db = self.notion.databases.retrieve(self.comments_db_id)
            print("[OK] Database commenti trovato!")

            print(f"Verifica accesso al database posts: {self.posts_db_id}")
            if self.posts_db_id: # Verifica solo se posts_db_id è definito
                posts_db = self.notion.databases.retrieve(self.posts_db_id)
                print("[OK] Database posts trovato!")
            else:
                print("[WARNING] Database posts non configurato specificamente (posts_db_id is None).")
            
        except Exception as e:
            print(f"\n[ERROR] Errore di connessione a Notion: {str(e)}")
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
            print(f"[OK] Contatto aggiunto con successo: {name}")
            return True, response
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante l'aggiunta del contatto: {error_msg}")
            return False, error_msg

    def add_comment(self, name, email, message, post_id, url=None, parent_id=None):
        """
        Aggiunge un nuovo commento al database, gestendo anche risposte e URL.
        """
        try:
            new_comment = {
                "Name": {"title": [{"text": {"content": name}}]},
                "Email": {"email": email},
                "Messaggio": {"rich_text": [{"text": {"content": message}}]},
                "Post ID": {"rich_text": [{"text": {"content": post_id}}]},
                "Data": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
                "Stato": {"select": {"name": "Nuovo"}} # Tutti i commenti necessitano di moderazione
            }

            if url:
                # Assicurati che la proprietà "URL" esista nel tuo database dei commenti
                new_comment["URL"] = {"url": url}
            
            if parent_id:
                # Assicurati che la proprietà "Parent Comment" esista per le risposte
                new_comment["Parent Comment"] = {"rich_text": [{"text": {"content": parent_id}}]}

            print(f"Tentativo di aggiunta commento per il post {post_id}")
            response = self.notion.pages.create(
                parent={"database_id": self.comments_db_id},
                properties=new_comment
            )
            print(f"Risposta da Notion API: {response}")
            print(f"[OK] Commento aggiunto con successo da: {name}. In attesa di moderazione.")
            return True, response
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante l'aggiunta del commento: {error_msg}")
            if "URL" in error_msg or "Parent Comment" in error_msg:
                print("[INFO]  Verifica che le proprietà 'URL' (tipo URL) e 'Parent Comment' (tipo Rich Text) esistano nel tuo database dei commenti in Notion.")
            return False, error_msg

    def get_blog_posts(self):
        """
        Recupera tutti i post pubblicati dal database Notion
        """
        try:
            response = self.notion.databases.query(
                database_id=self.posts_db_id,
                filter={
                    "property": "Stato",
                    "select": {
                        "equals": "Pubblicato"
                    }
                },
                sorts=[{
                    "property": "Data Pubblicazione", # MODIFICATO
                    "direction": "descending"
                }]
            )
            
            posts = []
            for page in response["results"]:
                properties = page["properties"]
                
                # Assicurati che i nomi delle proprietà corrispondano a quelli del tuo database "Articoli del Blog"
                title = properties.get("Titolo", {}).get("title", [{}])[0].get("text", {}).get("content", "Senza titolo")
                
                date_obj = properties.get("Data Pubblicazione", {}).get("date")
                date = date_obj["start"] if date_obj and date_obj.get("start") else datetime.now(timezone.utc).isoformat()
                
                # Per la lista dei post, usiamo la "Breve Descrizione" come contenuto
                short_description_list = properties.get("Breve Descrizione", {}).get("rich_text", [])
                content_summary = short_description_list[0].get("text", {}).get("content", "") if short_description_list and short_description_list[0].get("text") else ""
                
                post_id_list = properties.get("Post ID", {}).get("rich_text", [])
                post_id_val = post_id_list[0].get("text", {}).get("content", page["id"]) if post_id_list and post_id_list[0].get("text") else page["id"] # Fallback a page ID

                email_obj = properties.get("Email", {}).get("email") # 'Email' potrebbe non essere nei post
                email = email_obj if email_obj else ""

                stato_obj = properties.get("Stato", {}).get("select")
                stato = stato_obj["name"] if stato_obj and stato_obj.get("name") else ""
                
                posts.append({
                    "id": page["id"], # Notion Page ID
                    "title": title,
                    "date": date,
                    "content": content_summary, # Breve descrizione per la lista
                    "post_id": post_id_val, # Slug / ID personalizzato
                    "email": email,
                    "stato": stato
                })
            
            return True, posts
        except Exception as e:
            print(f"[ERROR] Errore nel recupero dei post: {str(e)}")
            return False, []

    def get_post_by_id(self, post_id):
        """
        Recupera un post specifico dal suo ID di pagina Notion.
        """
        try:
            # Ora usiamo pages.retrieve perché l'ID è l'ID della pagina
            response = self.notion.pages.retrieve(page_id=post_id)
            
            # Verifica se la pagina è stata trovata e se è pubblicata
            if not response:
                return False, None
            
            page = response
            properties = page.get("properties", {})
            
            stato_obj = properties.get("Stato", {}).get("select")
            stato = stato_obj.get("name") if stato_obj else ""
            
            if stato != "Pubblicato":
                print(f"Post con ID {post_id} trovato, ma non è pubblicato (stato: {stato}).")
                return False, None
            properties = page["properties"]

            # Assicurati che i nomi delle proprietà corrispondano a quelli del tuo database "Articoli del Blog"
            title = properties.get("Titolo", {}).get("title", [{}])[0].get("text", {}).get("content", "Senza titolo")

            date_obj = properties.get("Data Pubblicazione", {}).get("date")
            date = date_obj["start"] if date_obj and date_obj.get("start") else datetime.now(timezone.utc).isoformat()

            # Recupera il contenuto HTML dai blocchi "code" della pagina
            full_html_content = ""
            notion_page_id = page["id"]
            
            try:
                blocks_response = self.notion.blocks.children.list(block_id=notion_page_id)
                for block in blocks_response.get("results", []):
                    if block.get("type") == "code":
                        code_block = block.get("code", {})
                        rich_text_array = code_block.get("rich_text", [])
                        if rich_text_array and rich_text_array[0].get("type") == "text":
                            full_html_content += rich_text_array[0].get("text", {}).get("content", "")
            except Exception as e_blocks:
                print(f"Errore durante il recupero dei blocchi di contenuto per la pagina {notion_page_id}: {e_blocks}")
                # Continua con il contenuto vuoto o solo con le proprietà se i blocchi falliscono

            email_obj = properties.get("Email", {}).get("email")
            email = email_obj if email_obj else ""

            stato_obj = properties.get("Stato", {}).get("select")
            stato = stato_obj["name"] if stato_obj and stato_obj.get("name") else ""
            
            post_id_list = properties.get("Post ID", {}).get("rich_text", [])
            post_id_slug = post_id_list[0].get("text", {}).get("content", page["id"]) if post_id_list and post_id_list[0].get("text") else page["id"]

            post = {
                "id": notion_page_id, # Notion Page ID
                "title": title,
                "date": date,
                "content": full_html_content, # HTML completo dai blocchi code
                "post_id": post_id_slug, # Slug / ID personalizzato
                "email": email,
                "stato": stato
            }
            
            return True, post
        except Exception as e:
            print(f"[ERROR] Errore nel recupero del post: {str(e)}")
            return False, None

    def get_post_by_slug(self, slug):
        """
        Recupera un post specifico utilizzando il suo slug univoco.
        """
        try:
            # Cerca nel database un post con lo slug corrispondente
            response = self.notion.databases.query(
                database_id=self.posts_db_id,
                filter={
                    "property": "Post ID",
                    "rich_text": {
                        "equals": slug
                    }
                }
            )

            if not response.get("results"):
                print(f"Nessun post trovato con lo slug: {slug}")
                return False, None
            
            # Prendi il primo risultato (lo slug dovrebbe essere univoco)
            page = response["results"][0]
            
            # Una volta ottenuta la pagina, possiamo usare la logica di get_post_by_id per estrarre i dettagli
            # ma dobbiamo passare l'ID della pagina, non lo slug
            return self.get_post_by_id(page["id"])

        except Exception as e:
            print(f"[ERROR] Errore nel recupero del post con slug {slug}: {str(e)}")
            return False, None

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
            
            comments_flat = []
            for page in response['results']:
                props = page['properties']
                
                parent_id_list = props.get("Parent Comment", {}).get("rich_text", [])
                parent_id = parent_id_list[0].get("text", {}).get("content") if parent_id_list else None

                comments_flat.append({
                    'id': page['id'],
                    'name': props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'Anonimo'),
                    'message': props.get('Messaggio', {}).get('rich_text', [{}])[0].get('text', {}).get('content', ''),
                    'date': datetime.fromisoformat(props['Data']['date']['start'].replace('Z', '+00:00')) if props.get('Data') and props['Data'].get('date') and props['Data']['date'].get('start') else None,
                    'url': props.get('URL', {}).get('url'),
                    'parent_id': parent_id,
                    'children': []
                })
            
            # Costruisci la struttura ad albero
            comment_map = {c['id']: c for c in comments_flat}
            nested_comments = []
            for comment in comments_flat:
                if comment['parent_id'] and comment['parent_id'] in comment_map:
                    comment_map[comment['parent_id']]['children'].append(comment)
                else:
                    nested_comments.append(comment)

            print(f"[OK] Recuperati {len(comments_flat)} commenti approvati per il post {post_id}")
            return True, nested_comments
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante il recupero dei commenti: {error_msg}")
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
            
            contacts = []
            for page in response['results']:
                props = page['properties']
                contact = {
                    'name': props['Name']['title'][0]['text']['content'] if props['Name']['title'] else 'Anonimo',
                    'email': props['Email']['email'] if props['Email']['email'] else '',
                    'message': props['Messaggio']['rich_text'][0]['text']['content'] if props['Messaggio']['rich_text'] else '',
                    'company': props['Azienda']['rich_text'][0]['text']['content'] if 'Azienda' in props and props['Azienda']['rich_text'] else '',
                    'status': props['Stato']['select']['name'] if props['Stato']['select'] else 'Nuovo'
                }
                contacts.append(contact)
            
            print(f"[OK] Recuperati {len(contacts)} contatti")
            return contacts
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante il recupero dei contatti: {error_msg}")
            return []
            
    def get_all_comments(self):
        """
        Recupera tutti i commenti dal database
        """
        try:
            print(f"Tentativo di recupero commenti dal database: {self.comments_db_id}")
            response = self.notion.databases.query(
                database_id=self.comments_db_id,
                sorts=[{"property": "Data", "direction": "descending"}]
            )
            
            comments = []
            for page in response['results']:
                props = page['properties']
                comment = {
                    'id': page['id'],
                    'name': props['Name']['title'][0]['text']['content'] if props['Name']['title'] else 'Anonimo',
                    'email': props['Email']['email'] if props['Email']['email'] else '',
                    'message': props['Messaggio']['rich_text'][0]['text']['content'] if props['Messaggio']['rich_text'] else '',
                    'post_id': props['Post ID']['rich_text'][0]['text']['content'] if props['Post ID']['rich_text'] else '',
                    'date': props['Data']['date']['start'] if props['Data']['date'] else '',
                    'status': props['Stato']['select']['name'] if props['Stato']['select'] else 'Nuovo',
                    'url': props.get('URL', {}).get('url')
                }
                comments.append(comment)
            
            print(f"[OK] Recuperati {len(comments)} commenti")
            return comments
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante il recupero dei commenti: {error_msg}")
            return []

    def create_blog_posts_database(self, parent_page_id, db_name="Articoli del Blog"):
        """
        Crea un nuovo database Notion per i post del blog.
        """
        try:
            print(f"Tentativo di creazione database '{db_name}' sotto la pagina ID: {parent_page_id}")
            
            properties = {
                "Titolo": {"title": {}},
                "Post ID": {"rich_text": {}}, # Per lo slug o ID univoco del post
                "Contenuto": {"rich_text": {}}, # O potresti voler usare blocchi Notion per contenuti ricchi
                "Data Pubblicazione": {"date": {}},
                "Stato": {"select": {"options": [
                    {"name": "Bozza", "color": "gray"},
                    {"name": "Revisione", "color": "blue"},
                    {"name": "Pubblicato", "color": "green"},
                    {"name": "Archiviato", "color": "yellow"}
                ]}},
                "Autore": {"rich_text": {}},
                "Tags": {"multi_select": {"options": []}}, # Inizialmente vuoto, Notion permette di aggiungere opzioni al volo
                "Immagine Copertina URL": {"url": {}},
                "Breve Descrizione": {"rich_text": {}} # Per un riassunto/excerpt
            }

            title = [{"type": "text", "text": {"content": db_name}}]
            parent = {"type": "page_id", "page_id": parent_page_id}

            response = self.notion.databases.create(
                parent=parent,
                title=title,
                properties=properties
            )
            
            new_db_id = response.get("id")
            print(f"[OK] Database '{db_name}' creato con successo! ID: {new_db_id}")
            print(f"-->  Aggiungi questa riga al tuo file Config_Notion.env: NOTION_POSTS_DB_ID={new_db_id}")
            return True, new_db_id
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante la creazione del database '{db_name}': {error_msg}")
            if "Could not find a page with an ID" in error_msg:
                print("[INFO]  Assicurati che il Parent Page ID sia corretto e che l'integrazione Notion abbia accesso a quella pagina.")
            return False, error_msg

    def add_blog_post(self, title, html_content, author="Team Blog",
                      tags=None, status="Bozza", post_id_slug=None,
                      cover_image_url=None, short_description=None):
        """
        Aggiunge un nuovo post al database del blog in Notion.

        Args:
            title (str): Il titolo del post.
            html_content (str): Il contenuto HTML completo del post.
            author (str, optional): L'autore del post. Default "Team Blog".
            tags (list, optional): Una lista di stringhe per i tag. Default None.
            status (str, optional): Lo stato del post (es. "Bozza", "Pubblicato"). Default "Bozza".
            post_id_slug (str, optional): Un ID univoco o slug per il post. Se None, usa il page ID di Notion.
            cover_image_url (str, optional): URL dell'immagine di copertina.
            short_description (str, optional): Breve descrizione/excerpt del post.

        Returns:
            tuple: (bool, str) True e l'ID della pagina se ha successo, False e messaggio di errore altrimenti.
        """
        if not self.posts_db_id:
            return False, "ID del database dei post non configurato (NOTION_POSTS_DB_ID)."

        try:
            print(f"Tentativo di aggiunta post '{title}' al database: {self.posts_db_id}")
            
            page_properties = {
                "Titolo": {"title": [{"text": {"content": title}}]},
                "Data Pubblicazione": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
                "Stato": {"select": {"name": status}},
                "Autore": {"rich_text": [{"text": {"content": author}}]}
                # Rimuoviamo "HTML Content" dalle proprietà, lo metteremo nei blocchi children
            }

            if tags:
                page_properties["Tags"] = {"multi_select": [{"name": tag} for tag in tags]}
            
            if post_id_slug:
                page_properties["Post ID"] = {"rich_text": [{"text": {"content": post_id_slug}}]}

            if cover_image_url:
                page_properties["Immagine Copertina URL"] = {"url": cover_image_url}

            if short_description: # Assicurati che questa proprietà esista nel tuo DB
                page_properties["Breve Descrizione"] = {"rich_text": [{"text": {"content": short_description}}]}

            # Prepara i blocchi "code" per il contenuto HTML
            content_child_blocks = []
            chunk_size = 2000  # Limite per il contenuto di un rich_text all'interno di un blocco code
            
            for i in range(0, len(html_content), chunk_size):
                chunk = html_content[i:i + chunk_size]
                content_child_blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": chunk}}],
                        "language": "html"
                    }
                })

            response = self.notion.pages.create(
                parent={"database_id": self.posts_db_id},
                properties=page_properties,
                children=content_child_blocks # Aggiungiamo l'HTML come blocchi code
            )
            
            new_page_id = response.get("id")
            # Se non è stato fornito un post_id_slug, aggiorniamo la proprietà "Post ID" con il page_id.
            if not post_id_slug and new_page_id:
                 self.notion.pages.update(
                     page_id=new_page_id,
                     properties={"Post ID": {"rich_text": [{"text": {"content": new_page_id}}]}}
                 )
                 print(f"Proprietà 'Post ID' aggiornata con il Page ID: {new_page_id}")


            print(f"[OK] Post '{title}' aggiunto con successo! Page ID: {new_page_id}")
            return True, new_page_id
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante l'aggiunta del post '{title}': {error_msg}")
            # Potrebbe essere utile un debug più specifico per errori comuni
            if "Could not find property with name Titolo" in error_msg:
                print("[INFO]  Verifica che il database dei post abbia una proprietà 'Titolo' di tipo Title.")
            if "Unsaved transactions" in error_msg: # Errore comune con blocchi malformati
                print("[INFO]  Possibile problema con la formattazione dei 'content_blocks'. Verifica la struttura.")
            return False, error_msg

    def get_comments_for_moderation(self):
        """
        Recupera tutti i commenti con stato 'Nuovo' o 'Segnalato' per la moderazione.
        """
        try:
            print("Recupero commenti per la moderazione...")
            response = self.notion.databases.query(
                database_id=self.comments_db_id,
                filter={
                    "or": [
                        {"property": "Stato", "select": {"equals": "Nuovo"}},
                        {"property": "Stato", "select": {"equals": "Segnalato"}}
                    ]
                },
                sorts=[{"property": "Data", "direction": "ascending"}]
            )
            
            comments = []
            for page in response['results']:
                props = page['properties']
                comments.append({
                    'id': page['id'],
                    'name': props['Name']['title'][0]['text']['content'] if props['Name']['title'] else 'Anonimo',
                    'message': props['Messaggio']['rich_text'][0]['text']['content'] if props['Messaggio']['rich_text'] else '',
                    'post_id': props['Post ID']['rich_text'][0]['text']['content'] if props['Post ID']['rich_text'] else '',
                    'date': datetime.fromisoformat(props['Data']['date']['start'].replace('Z', '+00:00')),
                    'status': props['Stato']['select']['name']
                })
            
            print(f"[OK] Recuperati {len(comments)} commenti da moderare.")
            return True, comments
        except Exception as e:
            print(f"[ERROR] Errore durante il recupero dei commenti per la moderazione: {str(e)}")
            return False, []

    def update_comment_status(self, comment_id, status, moderator_notes=None):
        """
        Aggiorna lo stato di un commento e opzionalmente aggiunge note di moderazione.
        """
        try:
            print(f"Aggiornamento stato del commento {comment_id} a '{status}'")
            properties_to_update = {
                "Stato": {"select": {"name": status}}
            }
            
            if moderator_notes:
                # Assicurati che esista una proprietà "Note Moderatore" (Rich Text)
                properties_to_update["Note Moderatore"] = {"rich_text": [{"text": {"content": moderator_notes}}]}

            self.notion.pages.update(
                page_id=comment_id,
                properties=properties_to_update
            )
            print(f"[OK] Commento {comment_id} aggiornato con successo.")
            return True, "Stato aggiornato"
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante l'aggiornamento dello stato del commento {comment_id}: {error_msg}")
            if "Note Moderatore" in error_msg:
                print("[INFO]  Verifica che la proprietà 'Note Moderatore' (tipo Rich Text) esista nel tuo database.")
            return False, error_msg

    def update_post_content(self, page_id, new_html_content):
        """
        Aggiorna il contenuto di un post esistente, sostituendo i vecchi blocchi di codice.
        """
        try:
            # 1. Rimuovi tutti i blocchi esistenti dalla pagina
            existing_blocks = self.notion.blocks.children.list(block_id=page_id)
            for block in existing_blocks['results']:
                self.notion.blocks.delete(block_id=block['id'])

            # 2. Aggiungi i nuovi blocchi di contenuto HTML
            content_child_blocks = []
            chunk_size = 2000
            for i in range(0, len(new_html_content), chunk_size):
                chunk = new_html_content[i:i + chunk_size]
                content_child_blocks.append({
                    "object": "block",
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": chunk}}],
                        "language": "html"
                    }
                })
            
            self.notion.blocks.children.append(
                block_id=page_id,
                children=content_child_blocks
            )
            
            print(f"[OK] Contenuto del post {page_id} aggiornato con successo.")
            return True, page_id
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Errore durante l'aggiornamento del contenuto del post {page_id}: {error_msg}")
            return False, error_msg