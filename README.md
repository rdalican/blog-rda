# Blog Roberto D'Alicandro

Un blog personale sviluppato con Flask che racconta la mia esperienza e le mie riflessioni sul mondo dell'innovazione e dell'Intelligenza Artificiale.

## Caratteristiche

- Blog con articoli dinamici
- Sezione "Chi Sono" con il mio profilo professionale
- Sezione "Software Gratuito" per condividere risorse utili
- Design moderno e responsive con Tailwind CSS
- Visualizzazioni grafiche interattive con Chart.js

## Requisiti

- Python 3.8+
- Flask
- SQLAlchemy
- Altri requisiti sono elencati in `requirements.txt`

## Installazione

1. Clona il repository
```bash
git clone https://github.com/rdalican/blog-rda.git
cd blog-rda
```

2. Crea un ambiente virtuale e attivalo
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Installa le dipendenze
```bash
pip install -r requirements.txt
```

4. Avvia l'applicazione
```bash
python app.py
```

L'applicazione sarà disponibile all'indirizzo `http://localhost:5000`

## Struttura del Progetto

```
blog-rda/
├── app.py              # Applicazione Flask principale
├── templates/          # Template HTML
├── static/            
│   ├── images/        # Immagini
│   └── js/           # File JavaScript
├── requirements.txt    # Dipendenze Python
└── README.md          # Questo file
```

## Licenza

Tutti i diritti riservati - Roberto D'Alicandro