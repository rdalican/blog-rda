from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.environ.get('NOTION_TOKEN'))
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID')  # Usiamo il database dei contatti

post = {
    'Name': {'title': [{'text': {'content': 'Adattabilità & IA: Come Ballare con l\'Intelligenza Artificiale'}}]},
    'Messaggio': {'rich_text': [{'text': {'content': '''Mercato
Competenze
Educazione
Strategie
Il Paradosso dell'Adattabilità

Come ballare con l'Intelligenza Artificiale senza perdere il passo (e la testa!). Benvenuti nell'era in cui la nostra capacità di imparare e adattarci è la nostra risorsa più preziosa.

Il Nuovo Mercato del Lavoro: Trasformazione, non Apocalisse

L'IA sta ridisegnando il panorama professionale. Non si tratta di una semplice sostituzione, ma di una profonda riorganizzazione che crea nuove opportunità. I dati mostrano una crescita netta, spingendoci verso ruoli a maggior valore aggiunto.'''}}]},
    'Post ID': {'rich_text': [{'text': {'content': '1'}}]},
    'Stato': {'select': {'name': 'Pubblicato'}},
    'Data': {'date': {'start': '2024-01-01'}}
}

response = notion.pages.create(parent={'database_id': DATABASE_ID}, properties=post)
print('Post creato con successo!')