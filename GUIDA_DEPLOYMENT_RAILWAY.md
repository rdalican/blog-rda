# 🚂 Guida Completa al Deployment su Railway.app

## 📋 Indice
1. [Prerequisiti](#prerequisiti)
2. [Creazione Account Railway](#creazione-account-railway)
3. [Configurazione Progetto](#configurazione-progetto)
4. [Deploy dell'Applicazione](#deploy-dellapplicazione)
5. [Configurazione Variabili d'Ambiente](#configurazione-variabili-dambiente)
6. [Verifica e Test](#verifica-e-test)
7. [Costi e Monitoraggio](#costi-e-monitoraggio)
8. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisiti

Prima di iniziare, assicurati di avere:

- ✓ Un account GitHub (gratuito)
- ✓ Il repository Git del progetto già pushato su GitHub
- ✓ I database Notion già configurati e funzionanti
- ✓ Le credenziali email (Gmail App Password)
- ✓ Backup completo del progetto (eseguito con `create_backup.py`)

---

## 🎫 Creazione Account Railway

### Step 1: Registrazione

1. Vai su **https://railway.app**
2. Clicca su **"Start a New Project"** o **"Login"**
3. Scegli **"Login with GitHub"**
4. Autorizza Railway ad accedere al tuo account GitHub
5. Completa la registrazione

### Step 2: Verifica Email

1. Controlla la tua email
2. Verifica l'indirizzo email cliccando sul link ricevuto

### Step 3: Attivazione Piano Hobby

**IMPORTANTE per evitare limiti del piano Free:**

1. Vai su **Settings** → **Account**
2. Clicca su **"Upgrade to Hobby"**
3. Inserisci i dati della carta di credito/debito
   - **Non ti verrà addebitato nulla immediatamente**
   - Riceverai **$5 di crediti gratuiti** ogni mese
   - Pagherai solo se superi i $5/mese
4. Conferma l'upgrade

**💰 Costi Stimati:**
- Piano Hobby: **$0-5/mese** (con crediti gratuiti)
- Per il tuo blog con traffico basso: **~$3-5/mese**
- Nessun costo se rimani sotto i crediti gratuiti

---

## ⚙️ Configurazione Progetto

### Step 1: Push del Codice su GitHub

Se non l'hai già fatto, pusha il progetto su GitHub:

```bash
# Inizializza Git (se non già fatto)
git init

# Aggiungi tutti i file
git add .

# Crea il primo commit
git commit -m "Prepare for Railway deployment"

# Aggiungi il repository remoto (sostituisci con il tuo URL)
git remote add origin https://github.com/TUO_USERNAME/TUO_REPO.git

# Push su GitHub
git push -u origin main
```

### Step 2: Verifica File di Configurazione

Assicurati che questi file siano presenti nella root del progetto:

- ✓ `requirements.txt` - Dipendenze Python
- ✓ `Procfile` - Comando di avvio
- ✓ `runtime.txt` - Versione Python
- ✓ `railway.json` - Configurazione Railway
- ✓ `.env.example` - Template variabili d'ambiente
- ✓ `.gitignore` - File da ignorare (deve includere `.env`, `*.env`, `venv/`)

**Verifica `.gitignore`:**

```gitignore
# File sensibili
.env
*.env
Config_*.env

# Virtual environment
venv/
env/
ENV/

# Python cache
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/

# Backups
backups/
```

---

## 🚀 Deploy dell'Applicazione

### Step 1: Crea Nuovo Progetto

1. Nel dashboard Railway, clicca **"+ New Project"**
2. Seleziona **"Deploy from GitHub repo"**
3. Se richiesto, autorizza Railway ad accedere ai tuoi repository
4. Seleziona il repository del blog
5. Seleziona il branch `main` (o `master`)

### Step 2: Railway Rileva Automaticamente

Railway rileverà automaticamente:
- ✓ Che si tratta di un'app Python
- ✓ Il file `requirements.txt`
- ✓ Il file `Procfile`
- ✓ La versione Python da `runtime.txt`

### Step 3: Attendi il Build

1. Railway inizierà automaticamente il build
2. Puoi vedere i log in tempo reale
3. Il primo build richiede **2-5 minuti**

**⚠️ IMPORTANTE:** Il deploy FALLIRÀ finché non configuri le variabili d'ambiente!

---

## 🔐 Configurazione Variabili d'Ambiente

### Step 1: Accedi alle Variabili

1. Nel progetto Railway, clicca sulla tua app
2. Vai alla tab **"Variables"**
3. Clicca **"+ New Variable"**

### Step 2: Aggiungi TUTTE le Variabili

Copia i valori dal tuo file `.env` locale o `Config_*.env`:

#### Variabili Flask

```
SECRET_KEY=<genera_una_chiave_segreta_casuale>
PRODUCTION=true
PUBLIC_URL=https://tuo-dominio.railway.app
```

**Come generare SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Variabili Notion

```
NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_POSTS_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_COMMENTS_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_CONTACTS_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DOWNLOAD_DB_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Variabili Email

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tua-email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_DEFAULT_SENDER=tua-email@gmail.com
MAIL_RECIPIENT=tua-email@gmail.com
```

#### Variabile Admin

```
ADMIN_PASSWORD=your_secure_admin_password
```

### Step 3: Variabili Railway Automatiche

Railway imposta automaticamente:
- `RAILWAY_ENVIRONMENT=production`
- `PORT=<porta_automatica>`

**Non devi aggiungere queste manualmente!**

### Step 4: Salva e Rideploy

1. Dopo aver aggiunto tutte le variabili, clicca **"Deploy"**
2. Railway farà automaticamente il rideploy
3. Attendi il completamento (~2-3 minuti)

---

## 🌐 Configurazione Dominio

### Opzione 1: Dominio Railway Gratuito

1. Vai alla tab **"Settings"**
2. Nella sezione **"Domains"**
3. Clicca **"Generate Domain"**
4. Railway ti assegnerà un dominio tipo: `tuo-app.up.railway.app`
5. **Copia questo URL** e aggiornalo nella variabile `PUBLIC_URL`

### Opzione 2: Dominio Personalizzato (Opzionale)

Se hai un dominio tuo:

1. Nella sezione **"Domains"**, clicca **"Custom Domain"**
2. Inserisci il tuo dominio (es. `blog.tuosito.com`)
3. Railway ti darà un record CNAME da configurare
4. Vai nel pannello del tuo provider DNS
5. Aggiungi il record CNAME come indicato
6. Attendi la propagazione DNS (fino a 24h)

---

## ✅ Verifica e Test

### Step 1: Controlla i Log

1. Nella dashboard Railway, vai alla tab **"Deployments"**
2. Clicca sull'ultimo deployment
3. Controlla i log per errori

**Log di successo dovrebbe mostrare:**
```
--- RUNNING IN PRODUCTION MODE ---
[OK] Database contatti trovato!
[OK] Database commenti trovato!
[OK] Database posts trovato!
[OK] Database download trovato!
```

### Step 2: Testa l'Applicazione

Visita il tuo dominio Railway e verifica:

- ✓ Homepage carica correttamente
- ✓ Pagina `/blog` mostra i post
- ✓ Puoi aprire un singolo post
- ✓ Form di contatto funziona
- ✓ Sistema commenti funziona
- ✓ Download files funziona
- ✓ Login admin funziona (`/login`)

### Step 3: Test Completo

Esegui questi test:

1. **Test Post**: Apri un post e verifica immagini
2. **Test Commento**: Scrivi un commento e verifica email di moderazione
3. **Test Contatto**: Invia un messaggio dal form contatti
4. **Test Admin**:
   - Login su `/login`
   - Crea/modifica un post
   - Verifica upload immagini
5. **Test Download**: Scarica il file dalla pagina downloads

---

## 💰 Costi e Monitoraggio

### Dashboard di Monitoraggio

1. Vai su **Settings** → **Usage**
2. Qui puoi vedere:
   - CPU usage
   - Memory usage
   - Network bandwidth
   - Costi stimati del mese

### Limiti Piano Hobby

**Crediti mensili:** $5 gratis
**Cosa include:**
- 500 ore di esecuzione (~16 ore/giorno)
- 512MB RAM
- 1GB Disco
- 100GB Network

**Per il tuo blog:**
- Traffico: <1000 visite/mese
- Costo stimato: **$3-5/mese**
- **Probabilmente coperto dai crediti gratuiti!**

### Ottimizzazioni per Ridurre Costi

1. **Sleep Mode**: Railway può mettere in sleep l'app dopo inattività
   - Si risveglia al primo accesso (30-50 secondi)
   - Riduce i costi del 50-70%
   - Vai su Settings → Sleep Mode → Enable

2. **Monitoring**: Imposta alert per evitare sorprese
   - Settings → Notifications
   - Imposta alert a $4/mese

---

## 🔧 Troubleshooting

### Problema: Application Error / 503

**Causa:** Variabili d'ambiente mancanti o sbagliate

**Soluzione:**
1. Controlla i log: Tab "Deployments" → Ultimo deploy → View Logs
2. Cerca errori tipo `KeyError` o `ValueError`
3. Verifica tutte le variabili d'ambiente
4. Rideploy dopo aver corretto

---

### Problema: Notion Integration Error

**Errore nei log:**
```
[WARNING] Impossibile accedere al database posts
```

**Soluzione:**
1. Verifica `NOTION_TOKEN` sia corretto
2. Verifica gli ID dei database
3. Assicurati che l'integrazione Notion abbia accesso ai database:
   - Apri ogni database in Notion
   - Clicca sui 3 puntini in alto a destra
   - "Connections" → Aggiungi la tua integrazione

---

### Problema: Email Non Inviate

**Errore:**
```
CRITICAL: Failed to send moderation email
```

**Soluzione Gmail:**
1. Vai su https://myaccount.google.com/apppasswords
2. Crea una nuova "App Password"
3. Usa QUELLA password in `MAIL_PASSWORD` (non la password Gmail normale)
4. Verifica che `MAIL_USE_TLS=True`

**Alternative a Gmail:**
- SendGrid (piano free: 100 email/giorno)
- Mailgun (piano free: 5000 email/mese)

---

### Problema: Immagini Non Caricate

**Causa:** URL base sbagliato

**Soluzione:**
1. Verifica la variabile `PUBLIC_URL` sia impostata correttamente
2. Deve essere: `https://tuo-dominio.railway.app` (SENZA trailing slash)
3. Rideploy dopo la modifica

---

### Problema: Upload Immagini Non Funziona

**Causa:** Railway non ha storage persistente

**Soluzione:**
Le immagini uploadate tramite `/admin/upload_image` vengono salvate in `/static/images/`, ma Railway può resettare i file ad ogni deploy.

**Opzioni:**
1. **Usa Cloudinary** (raccomandato, piano free generoso):
   - Registrati su https://cloudinary.com
   - Integra nel codice per upload immagini

2. **Usa Railway Volumes** (storage persistente):
   - Settings → Volumes → Add Volume
   - Mount path: `/app/static/images`
   - Costo: ~$0.25/GB/mese

---

### Problema: Build Fallisce

**Errore:** `Failed to build`

**Soluzioni comuni:**
1. Verifica `requirements.txt` sia corretto
2. Verifica `runtime.txt` contenga `python-3.11.9`
3. Controlla che non ci siano errori di sintassi in `blog_app.py`
4. Guarda i build logs per dettagli specifici

---

## 📞 Supporto

### Risorse Utili

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Flask Docs**: https://flask.palletsprojects.com
- **Notion API Docs**: https://developers.notion.com

### In Caso di Problemi Gravi

1. **Rollback**: Nella tab "Deployments", clicca su un deployment precedente funzionante e clicca "Redeploy"

2. **Controlla i Logs**: Sempre controllare i logs per capire l'errore esatto

3. **Ripristina Backup**: Se tutto fallisce, hai il backup creato con `create_backup.py`

---

## 🎉 Congratulazioni!

Se hai seguito tutti i passi, il tuo blog è ora online su Railway!

### Prossimi Passi

1. ✓ **Dominio Personalizzato**: Considera di collegare un tuo dominio
2. ✓ **SSL/HTTPS**: Railway fornisce HTTPS automaticamente
3. ✓ **Monitoring**: Imposta alert per monitorare uptime e costi
4. ✓ **Backup Automatici**: Considera di schedulare backup settimanali
5. ✓ **CDN**: Per traffico alto, considera Cloudflare (gratuito)

---

## 💡 Pro Tips

### Auto-Deploy da GitHub

Railway può fare auto-deploy ad ogni push su GitHub:

1. Settings → GitHub → Auto Deploy
2. Seleziona il branch (es. `main`)
3. Ogni volta che fai `git push`, Railway rideploya automaticamente

### Logging Avanzato

Per log migliori in produzione, aggiungi a `blog_app.py`:

```python
import logging

if IS_PRODUCTION:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
```

### Health Check Endpoint

Railway può monitorare la salute dell'app. Aggiungi in `blog_app.py`:

```python
@app.route('/health')
def health_check():
    return {'status': 'healthy'}, 200
```

Poi in Settings → Health Check → `/health`

---

**Buon deployment! 🚀**
