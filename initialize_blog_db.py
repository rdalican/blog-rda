import os
from notion_manager import NotionManager
from dotenv import load_dotenv

def main():
    """
    Script per creare il database dei post del blog in Notion.
    """
    # Carica le variabili d'ambiente da Config_Notion.env
    # Assicurati che il file Config_Notion.env sia nella stessa directory
    # o fornisci il percorso corretto a load_dotenv.
    config_path = 'Config_Notion.env'
    if not os.path.exists(config_path):
        print(f"Errore: File di configurazione '{config_path}' non trovato.")
        print("Assicurati che esista e contenga NOTION_TOKEN e NOTION_DATABASE_ID (per i contatti).")
        return

    load_dotenv(config_path)
    print(f"Caricato {config_path}")

    # Parametri per il nuovo database
    # L'ID della pagina genitore sotto cui creare il database
    parent_page_id = "1fd2c37023cf80ad884af85018c7c11e"
    # Il nome che vuoi dare al nuovo database
    database_name = "Articoli del Blog"

    print(f"\nInizializzazione di NotionManager...")
    try:
        manager = NotionManager()
        print("NotionManager inizializzato con successo.")
    except Exception as e:
        print(f"Errore durante l'inizializzazione di NotionManager: {e}")
        print("Controlla che NOTION_TOKEN sia valido e che l'integrazione abbia accesso ai database specificati in Config_Notion.env.")
        return

    print(f"\nTentativo di creare il database '{database_name}' sotto la pagina ID: {parent_page_id}")
    
    success, result = manager.create_blog_posts_database(
        parent_page_id=parent_page_id,
        db_name=database_name
    )

    if success:
        new_db_id = result
        print(f"\n🎉 Database '{database_name}' creato con successo!")
        print(f"   ID del nuovo database: {new_db_id}")
        print(f"\n➡️  AZIONE RICHIESTA: Aggiungi la seguente riga al tuo file '{config_path}':")
        print(f"   NOTION_POSTS_DB_ID={new_db_id}")
        print("\nDopo aver aggiunto l'ID, il tuo blog utilizzerà questo nuovo database per i post.")
    else:
        print(f"\n❌ Fallimento nella creazione del database '{database_name}'.")
        print(f"   Errore: {result}")
        if "Could not find a page with an ID" in str(result):
             print("   Suggerimento: Verifica che il 'Parent Page ID' sia corretto e che la tua integrazione Notion")
             print("   abbia i permessi necessari per accedere e creare contenuti sotto quella pagina.")
        elif "Invalid request" in str(result):
            print("   Suggerimento: Potrebbe esserci un problema con i parametri inviati o con i permessi dell'integrazione.")

if __name__ == "__main__":
    main()