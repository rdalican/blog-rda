#!/usr/bin/env python3
"""
Script di backup completo per il blog Flask/Notion
Esegue backup di:
- Tutte le configurazioni (.env files)
- File statici (images, files)
- Templates
- Database Notion (esportazione JSON)
- Codice sorgente
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from notion_manager import NotionManager

# Carica le variabili d'ambiente
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'Config_Email.env'))
load_dotenv(os.path.join(basedir, 'Config_Notion.env'))

def create_backup():
    """Crea un backup completo del progetto"""

    # Crea la directory di backup con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path('backups') / f'backup_{timestamp}'
    backup_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== CREAZIONE BACKUP: {backup_dir} ===\n")

    # 1. Backup configurazioni
    print("[1/6] Backup configurazioni...")
    config_dir = backup_dir / 'config'
    config_dir.mkdir(exist_ok=True)

    config_files = ['Config_Email.env', 'Config_Notion.env', '.env', 'requirements.txt']
    for config_file in config_files:
        if Path(config_file).exists():
            shutil.copy2(config_file, config_dir / config_file)
            print(f"  OK {config_file}")

    # 2. Backup file statici
    print("\n[2/6] Backup file statici...")
    static_backup = backup_dir / 'static'
    if Path('static').exists():
        shutil.copytree('static', static_backup, dirs_exist_ok=True)

        # Conta i file
        files_count = sum(1 for _ in static_backup.rglob('*') if _.is_file())
        print(f"  OK {files_count} file copiati da /static")

    # 3. Backup templates
    print("\n[3/6] Backup templates...")
    templates_backup = backup_dir / 'templates'
    if Path('templates').exists():
        shutil.copytree('templates', templates_backup, dirs_exist_ok=True)
        templates_count = sum(1 for _ in templates_backup.rglob('*.html'))
        print(f"  OK {templates_count} template HTML copiati")

    # 4. Backup codice sorgente
    print("\n[4/6] Backup codice sorgente...")
    source_backup = backup_dir / 'source'
    source_backup.mkdir(exist_ok=True)

    source_files = ['blog_app.py', 'notion_manager.py', 'wsgi.py']
    for source_file in source_files:
        if Path(source_file).exists():
            shutil.copy2(source_file, source_backup / source_file)
            print(f"  OK {source_file}")

    # 5. Backup dati Notion (esportazione JSON)
    print("\n[5/6] Backup dati da Notion...")
    notion_backup_dir = backup_dir / 'notion_data'
    notion_backup_dir.mkdir(exist_ok=True)

    try:
        notion = NotionManager()

        # Backup post del blog
        success, posts = notion.get_blog_posts()
        if success:
            with open(notion_backup_dir / 'blog_posts.json', 'w', encoding='utf-8') as f:
                json.dump(posts, f, ensure_ascii=False, indent=2, default=str)
            print(f"  OK {len(posts)} post del blog esportati")

        # Backup commenti
        comments = notion.get_all_comments()
        if comments:
            with open(notion_backup_dir / 'comments.json', 'w', encoding='utf-8') as f:
                json.dump(comments, f, ensure_ascii=False, indent=2, default=str)
            print(f"  OK {len(comments)} commenti esportati")

        # Backup contatti
        contacts = notion.get_contacts()
        if contacts:
            with open(notion_backup_dir / 'contacts.json', 'w', encoding='utf-8') as f:
                json.dump(contacts, f, ensure_ascii=False, indent=2, default=str)
            print(f"  OK {len(contacts)} contatti esportati")

    except Exception as e:
        print(f"  WARNING: Errore durante il backup Notion: {e}")
        print("  Il backup continuera' senza i dati Notion")

    # 6. Crea file di manifest
    print("\n[6/6] Creazione manifest del backup...")
    manifest = {
        'backup_timestamp': timestamp,
        'backup_date': datetime.now().isoformat(),
        'python_version': '3.13',
        'databases': {
            'notion_posts_db': os.getenv('NOTION_POSTS_DB_ID'),
            'notion_comments_db': os.getenv('NOTION_COMMENTS_DB_ID'),
            'notion_contacts_db': os.getenv('NOTION_CONTACTS_DB_ID'),
            'notion_download_db': os.getenv('NOTION_DOWNLOAD_DB_ID')
        },
        'files_backed_up': {
            'config': len(list((backup_dir / 'config').glob('*'))) if (backup_dir / 'config').exists() else 0,
            'static': sum(1 for _ in static_backup.rglob('*') if _.is_file()) if static_backup.exists() else 0,
            'templates': sum(1 for _ in templates_backup.rglob('*') if _.is_file()) if templates_backup.exists() else 0,
            'source': len(list((backup_dir / 'source').glob('*'))) if (backup_dir / 'source').exists() else 0
        }
    }

    with open(backup_dir / 'MANIFEST.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Crea README del backup
    readme_content = f"""# BACKUP del Blog RdA

Data backup: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Timestamp: {timestamp}

## Contenuto del backup:

### Configurazioni (/config)
- Config_Email.env
- Config_Notion.env
- requirements.txt

### File Statici (/static)
- Immagini del blog
- File per download
- CSS e JavaScript

### Templates (/templates)
- Tutti i template HTML

### Codice Sorgente (/source)
- blog_app.py
- notion_manager.py
- wsgi.py

### Dati Notion (/notion_data)
- blog_posts.json (tutti i post)
- comments.json (tutti i commenti)
- contacts.json (tutti i contatti)

## Database Notion ID:
- Posts: {os.getenv('NOTION_POSTS_DB_ID')}
- Comments: {os.getenv('NOTION_COMMENTS_DB_ID')}
- Contacts: {os.getenv('NOTION_CONTACTS_DB_ID')}
- Downloads: {os.getenv('NOTION_DOWNLOAD_DB_ID')}

## Per ripristinare:
1. Ripristina i file .env nella directory principale
2. Ricrea i database Notion usando gli ID sopra
3. Importa i dati JSON nei database Notion
4. Ripristina i file statici e templates
5. Ricopia il codice sorgente

## Note:
- Questo backup NON include il virtual environment (venv/)
- I database Notion devono essere ricreati manualmente o gli ID aggiornati
- Verifica che tutte le API key siano ancora valide
"""

    with open(backup_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print("\n" + "="*50)
    print("BACKUP COMPLETATO CON SUCCESSO!")
    print("="*50)
    print(f"\nPercorso backup: {backup_dir.absolute()}")
    print(f"\nDimensione totale: {get_dir_size(backup_dir) / (1024*1024):.2f} MB")
    print("\nFile creati:")
    print(f"  - MANIFEST.json (informazioni sul backup)")
    print(f"  - README.md (istruzioni di ripristino)")
    print(f"  - /config (configurazioni)")
    print(f"  - /static (file statici)")
    print(f"  - /templates (template HTML)")
    print(f"  - /source (codice sorgente)")
    print(f"  - /notion_data (dati esportati)")

    return backup_dir

def get_dir_size(path):
    """Calcola la dimensione totale di una directory"""
    return sum(f.stat().st_size for f in Path(path).rglob('*') if f.is_file())

if __name__ == '__main__':
    try:
        backup_path = create_backup()
        print(f"\nOK - Backup salvato in: {backup_path.absolute()}")
        print("\nPuoi comprimere questa cartella per archiviarla.")
    except Exception as e:
        print(f"\nERRORE durante il backup: {e}")
        import traceback
        traceback.print_exc()
