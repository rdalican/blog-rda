import os
from notion_manager import NotionManager
from dotenv import load_dotenv
from datetime import datetime, timezone

def main():
    """
    Script per creare il primo post del blog sull'adattabilità e IA nel database Notion.
    """
    config_path = 'Config_Notion.env'
    if not os.path.exists(config_path):
        print(f"Errore: File di configurazione '{config_path}' non trovato.")
        return
    load_dotenv(config_path)
    print(f"Caricato {config_path}")

    try:
        manager = NotionManager()
        print("NotionManager inizializzato con successo.")
    except Exception as e:
        print(f"Errore durante l'inizializzazione di NotionManager: {e}")
        return

    post_title = "Adattabilità & IA: Come ballare con l'Intelligenza Artificiale senza perdere il passo (e la testa!)"
    post_author = "RdA" # Puoi cambiarlo se preferisci
    post_tags = ["Adattabilità", "Intelligenza Artificiale", "Futuro del Lavoro", "Innovazione", "Mercato del Lavoro", "Competenze"]
    post_status = "Pubblicato" # O "Bozza" se preferisci revisionarlo prima
    post_slug = "adattabilita-ia-primo-post"
    post_short_description = "Esploriamo come l'adattabilità sia la chiave per navigare il cambiamento portato dall'Intelligenza Artificiale nel mondo del lavoro e oltre."
    # post_cover_image_url = "URL_IMMAGINE_COPERTINA_SE_NE_HAI_UNA"

    post_html_content = """
    <main class="container mx-auto px-6 py-8">
        
        <section id="paradosso" class="text-center py-16">
            <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">Il Paradosso dell'Adattabilità</h2>
            <p class="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto">Come ballare con l'Intelligenza Artificiale senza perdere il passo (e la testa!). Benvenuti nell'era in cui la nostra capacità di imparare e adattarci è la nostra risorsa più preziosa.</p>
        </section>

        <section id="mercato" class="content-section">
            <h3 class="section-title">Il Nuovo Mercato del Lavoro: Trasformazione, non Apocalisse</h3>
            <p class="section-subtitle">L'IA sta ridisegnando il panorama professionale. Non si tratta di una semplice sostituzione, ma di una profonda riorganizzazione che crea nuove opportunità. I dati mostrano una crescita netta, spingendoci verso ruoli a maggior valore aggiunto.</p>
            
            <div class="grid md:grid-cols-2 gap-12 items-center mt-12">
                <div class="fade-in">
                    <h4 class="text-xl font-semibold text-center mb-4">Impatto sul Lavoro (Stime WEF 2025)</h4>
                    <div class="chart-container">
                        <canvas id="jobMarketChart"></canvas>
                    </div>
                </div>
                <div class="text-gray-700 space-y-6 fade-in">
                    <div class="card border-l-4 border-blue-500">
                        <h4 class="font-bold text-lg">Un Bilancio Positivo</h4>
                        <p>Anche se circa 85 milioni di ruoli potrebbero essere trasformati o sostituiti, si prevede la creazione di 97 milioni di nuovi posti di lavoro. Questo indica una crescita netta e un'evoluzione delle professioni.</p>
                    </div>
                    <div class="card border-l-4 border-teal-500">
                        <h4 class="font-bold text-lg">Focus sull'Integrazione</h4>
                        <p>Come sottolinea l'Organizzazione Internazionale del Lavoro (ILO), l'IA generativa è destinata a "integrare" più che a "distruggere" i posti di lavoro, potenziando le capacità umane e automatizzando i compiti di routine.</p>
                    </div>
                </div>
            </div>

            <div class="mt-20">
                 <h4 class="text-2xl font-bold text-center mb-8 text-gray-900">Professioni in Evoluzione e Nuovi Ruoli</h4>
                 <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 fade-in">
                    <div class="card card-hover">
                        <h5 class="font-bold text-blue-600">Ingegnere Fintech</h5>
                        <p class="text-sm text-gray-600 mt-2">Fonde finanza e IA per innovare servizi finanziari, implementando soluzioni algoritmiche per trading, gestione del rischio e servizi al cliente.</p>
                    </div>
                    <div class="card card-hover">
                        <h5 class="font-bold text-blue-600">Specialista Trasformazione Digitale</h5>
                        <p class="text-sm text-gray-600 mt-2">Guida le aziende nell'adozione di tecnologie IA per ottimizzare i processi, migliorare l'efficienza e creare nuovo valore di business.</p>
                    </div>
                    <div class="card card-hover">
                        <h5 class="font-bold text-blue-600">Eticista dell'IA</h5>
                        <p class="text-sm text-gray-600 mt-2">Un ruolo cruciale che valuta le implicazioni morali e sociali dell'IA, sviluppando linee guida per un uso equo e responsabile.</p>
                    </div>
                    <div class="card card-hover">
                        <h5 class="font-bold text-blue-600">Analista Sicurezza IA</h5>
                        <p class="text-sm text-gray-600 mt-2">Utilizza tecniche di machine learning per rilevare, prevedere e neutralizzare minacce informatiche in tempo reale, proteggendo i dati sensibili.</p>
                    </div>
                    <div class="card card-hover">
                        <h5 class="font-bold text-blue-600">Diagnostica Medica Potenziata</h5>
                        <p class="text-sm text-gray-600 mt-2">Medici e ricercatori usano l'IA per analizzare immagini mediche (TAC, raggi X) con una precisione sovrumana, accelerando le diagnosi.</p>
                    </div>
                    <div class="card card-hover">
                        <h5 class="font-bold text-blue-600">Creativo Generativo</h5>
                        <p class="text-sm text-gray-600 mt-2">Artisti, designer e scrittori usano l'IA come partner creativo per generare idee, bozzetti, musiche e testi, espandendo i confini della creatività.</p>
                    </div>
                 </div>
            </div>
        </section>

        <section id="competenze" class="content-section bg-white rounded-xl shadow-lg">
            <h3 class="section-title">Le Competenze del Futuro: Cuore, Cervello e Furbizia</h3>
            <p class="section-subtitle">Mentre l'IA gestisce i dati, il nostro valore risiede nelle capacità unicamente umane. La tecnologia è il copilota, ma noi restiamo al comando della strategia, della creatività e dell'etica.</p>
            
            <div class="grid lg:grid-cols-3 gap-8 mt-12">
                <div class="lg:col-span-1 space-y-4">
                    <div data-skill="critico" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer">
                        <h4 class="font-bold">Pensiero Critico</h4>
                        <p class="text-sm text-gray-600">Analizzare, interpretare e porre le domande giuste.</p>
                    </div>
                    <div data-skill="creativita" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer">
                        <h4 class="font-bold">Creatività e Innovazione</h4>
                        <p class="text-sm text-gray-600">Generare idee originali e soluzioni non convenzionali.</p>
                    </div>
                    <div data-skill="agilita" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer">
                        <h4 class="font-bold">Agilità di Apprendimento</h4>
                        <p class="text-sm text-gray-600">Imparare rapidamente e adattarsi al cambiamento costante.</p>
                    </div>
                     <div data-skill="empatia" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer">
                        <h4 class="font-bold">Empatia e Intelligenza Emotiva</h4>
                        <p class="text-sm text-gray-600">Comprendere gli altri, collaborare e guidare con umanità.</p>
                    </div>
                    <div data-skill="prompt" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer">
                        <h4 class="font-bold">Prompt Engineering</h4>
                        <p class="text-sm text-gray-600">L'arte di dialogare con l'IA per ottenere i risultati migliori.</p>
                    </div>
                </div>
                <div class="lg:col-span-2 bg-gray-100 p-8 rounded-lg flex items-center fade-in">
                    <div id="skill-description">
                        <h4 class="text-xl font-bold mb-2">Seleziona una competenza</h4>
                        <p>Clicca su una delle competenze a sinistra per scoprire perché è fondamentale nell'era dell'Intelligenza Artificiale e come puoi iniziare a svilupparla oggi stesso.</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="educazione" class="content-section">
            <h3 class="section-title">L'Educazione si Reinventa: Dalla Cattedra al Campo Gioco</h3>
            <p class="section-subtitle">Il vecchio modello basato sulla memorizzazione lascia il posto a un approccio dinamico. L'obiettivo non è più sapere tutto, ma saper imparare, de-imparare e ri-imparare costantemente.</p>
            
            <div class="grid md:grid-cols-2 gap-8 mt-12">
                <div class="card fade-in">
                    <h4 class="text-2xl font-bold mb-4 text-red-600">Modello Tradizionale (Obsoleto)</h4>
                    <ul class="space-y-3 text-gray-700 list-disc">
                        <li>Focus sulla memorizzazione di fatti.</li>
                        <li>Apprendimento "una tantum" per una carriera.</li>
                        <li>Discipline isolate e insegnamento frontale.</li>
                        <li>La conoscenza è un prodotto finito.</li>
                    </ul>
                </div>
                <div class="bg-blue-600 text-white p-8 rounded-lg shadow-lg fade-in">
                    <h4 class="text-2xl font-bold mb-4">Nuovo Paradigma (Adattivo)</h4>
                    <ul class="space-y-3 list-disc">
                        <li>Focus sull'esplorazione e il pensiero critico.</li>
                        <li>Apprendimento permanente (Lifelong Learning).</li>
                        <li>Approccio transdisciplinare e basato su problemi.</li>
                        <li>La conoscenza è un processo dinamico.</li>
                    </ul>
                </div>
            </div>
        </section>

        <section id="strategie" class="content-section">
            <h3 class="section-title">La Tua Guida alla Sopravvivenza (e al Successo)</h3>
            <p class="section-subtitle">Affrontare il cambiamento richiede una strategia. Ecco come individui e organizzazioni possono non solo sopravvivere, ma prosperare affilando costantemente i propri strumenti.</p>
            
            <div class="mt-12 fade-in">
                <h4 class="text-xl font-bold mb-4 text-center md:text-left">La Tua Cassetta degli Attrezzi Personale</h4>
                <div class="grid md:grid-cols-2 gap-8 items-start">
                    <ul class="space-y-4">
                        <li class="flex items-start">
                            <span class="text-blue-500 mr-3 mt-1">&#10003;</span>
                            <span><strong class="text-gray-900">Coltiva la Mentalità di Crescita:</strong> Abbraccia le sfide, impara dai fallimenti e mantieni la curiosità. È il tuo sistema operativo per l'adattabilità.</span>
                        </li>
                        <li class="flex items-start">
                             <span class="text-blue-500 mr-3 mt-1">&#10003;</span>
                            <span><strong class="text-gray-900">Sperimenta con il Micro-learning:</strong> Usa app e moduli brevi per imparare qualcosa di nuovo ogni giorno, anche solo per 15 minuti.</span>
                        </li>
                         <li class="flex items-start">
                            <span class="text-blue-500 mr-3 mt-1">&#10003;</span>
                            <span><strong class="text-gray-900">Impara Facendo (Project-Based Learning):</strong> Crea un piccolo progetto basato sull'IA. L'esperienza pratica è il modo più rapido per consolidare le competenze.</span>
                        </li>
                         <li class="flex items-start">
                             <span class="text-blue-500 mr-3 mt-1">&#10003;</span>
                            <span><strong class="text-gray-900">Diventa un "Problem-Solver":</strong> Allenati con puzzle, giochi di strategia o escape room. Sviluppano il pensiero critico e la capacità di risolvere problemi complessi.</span>
                        </li>
                    </ul>
                    <div class="card bg-gray-50">
                        <h4 class="font-bold text-lg mb-2">Metafora: Affilare l'Ascia</h4>
                        <p class="text-gray-600">"Se avessi otto ore per abbattere un albero, ne passerei sei ad affilare l'ascia." - Abraham Lincoln. Investire tempo nell'apprendimento (affilare l'ascia) non è una perdita di tempo, ma la strategia più efficace per ottenere risultati migliori con meno sforzo. Il reskilling e l'upskilling sono la tua affilatura quotidiana.</p>
                    </div>
                </div>
            </div>
        </section>

    </main>
""".format(title=post_title, year=datetime.now().year)

    print(f"\nTentativo di creare il post: '{post_title}'")
    
    success, result = manager.add_blog_post(
        title=post_title,
        html_content=post_html_content,
        author=post_author,
        tags=post_tags,
        status=post_status,
        post_id_slug=post_slug,
        short_description=post_short_description
        # cover_image_url=post_cover_image_url # Uncomment if you have one
    )

    if success:
        new_page_id = result
        print(f"\n🎉 Post '{post_title}' creato con successo nel database 'Articoli del Blog'!")
        print(f"   ID della nuova pagina: {new_page_id}")
        print(f"   Puoi visualizzarlo e modificarlo in Notion.")
        print(f"   È stato creato come '{post_status}'.")
    else:
        print(f"\n❌ Fallimento nella creazione del post '{post_title}'.")
        print(f"   Errore: {result}")

if __name__ == "__main__":
    main()