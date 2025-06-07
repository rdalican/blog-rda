import os
from notion_manager import NotionManager
from dotenv import load_dotenv
from datetime import datetime, timezone

# Rimuoviamo create_content_blocks() perché useremo HTML diretto

def main():
    """
    Script per creare il post sull'adattabilità nel database Notion, usando HTML diretto.
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

    post_title = "Il Paradosso dell'Adattabilità: Ballare con l'IA senza Perdere il Passo (e la Testa!)"
    post_author = "Kilo Code (con un pizzico di IA)"
    post_tags = ["Adattabilità", "Intelligenza Artificiale", "Futuro del Lavoro", "Sviluppo Personale", "Innovazione", "Humor"]
    post_status = "Bozza" # Mettilo in Bozza così puoi controllarlo
    post_slug = "adattabilita-ia-post-elegante-scherzoso-html" # Aggiunto -html per distinguerlo
    post_short_description = "Un viaggio ironico ma profondo nell'era dell'IA, scoprendo come l'adattabilità sia la nostra migliore alleata. Versione HTML."
    # post_cover_image_url = "URL_IMMAGINE_COPERTINA_SE_CE_LHAI" # Aggiungi un URL se hai un'immagine

    # Contenuto HTML completo del post
    post_html_content = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Interattiva: Adattabilità nell'Era dell'IA</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            height: 300px;
            max-height: 400px;
        }
        @media (min-width: 768px) {
            .chart-container {
                height: 350px;
            }
        }
        .nav-link {
            transition: color 0.3s, border-bottom-color 0.3s;
            border-bottom: 2px solid transparent;
        }
        .nav-link:hover, .nav-link.active {
            color: #3b82f6; /* blue-500 */
            border-bottom-color: #3b82f6;
        }
        .skill-card.active {
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3), 0 4px 6px -2px rgba(59, 130, 246, 0.2);
            border-color: #3b82f6;
        }
        .fade-in {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.6s ease-out, transform 0.6s ease-out;
        }
        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">

    <header class="bg-white/80 backdrop-blur-md sticky top-0 z-50 shadow-sm">
        <nav class="container mx-auto px-6 py-3 flex justify-between items-center">
            <h1 class="text-xl font-bold text-gray-800">Adattabilità & IA</h1>
            <div class="hidden md:flex space-x-8">
                <a href="#mercato" class="nav-link">Mercato</a>
                <a href="#competenze" class="nav-link">Competenze</a>
                <a href="#educazione" class="nav-link">Educazione</a>
                <a href="#strategie" class="nav-link">Strategie</a>
            </div>
        </nav>
    </header>

    <main class="container mx-auto px-6 py-8">
        
        <section id="hero" class="text-center py-16">
            <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">Il Paradosso dell'Adattabilità</h2>
            <p class="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto">Come ballare con l'Intelligenza Artificiale senza perdere il passo (e la testa!). Benvenuti nell'era in cui la nostra capacità di imparare e adattarci è la nostra risorsa più preziosa.</p>
        </section>

        <section id="mercato" class="py-16">
            <div class="text-center mb-12">
                <h3 class="text-3xl font-bold text-gray-900">Il Nuovo Mercato del Lavoro: Trasformazione, non Apocalisse</h3>
                <p class="text-gray-600 mt-2 max-w-2xl mx-auto">L'IA sta ridisegnando il panorama professionale. Non si tratta di una semplice sostituzione, ma di una profonda riorganizzazione che crea nuove opportunità. I dati mostrano una crescita netta, spingendoci verso ruoli a maggior valore aggiunto.</p>
            </div>
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div class="fade-in">
                    <h4 class="text-xl font-semibold text-center mb-4">Impatto sul Lavoro (Stime WEF 2025)</h4>
                    <div class="chart-container">
                        <canvas id="jobMarketChart"></canvas>
                    </div>
                </div>
                <div class="text-gray-700 space-y-4 fade-in">
                    <div class="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
                        <h4 class="font-bold text-lg">Un Bilancio Positivo</h4>
                        <p>Anche se circa 85 milioni di ruoli potrebbero essere trasformati o sostituiti, si prevede la creazione di 97 milioni di nuovi posti di lavoro. Questo indica una crescita netta e un'evoluzione delle professioni.</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md border-l-4 border-teal-500">
                        <h4 class="font-bold text-lg">Focus sull'Integrazione</h4>
                        <p>Come sottolinea l'Organizzazione Internazionale del Lavoro (ILO), l'IA generativa è destinata a "integrare" più che a "distruggere" i posti di lavoro, potenziando le capacità umane e automatizzando i compiti di routine.</p>
                    </div>
                </div>
            </div>

            <div class="mt-20">
                 <h4 class="text-2xl font-bold text-center mb-8 text-gray-900">Professioni in Evoluzione e Nuovi Ruoli</h4>
                 <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 fade-in">
                    <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
                        <h5 class="font-bold text-blue-600">Ingegnere Fintech</h5>
                        <p class="text-sm text-gray-600 mt-2">Fonde finanza e IA per innovare servizi finanziari, implementando soluzioni algoritmiche per trading, gestione del rischio e servizi al cliente.</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
                        <h5 class="font-bold text-blue-600">Specialista Trasformazione Digitale</h5>
                        <p class="text-sm text-gray-600 mt-2">Guida le aziende nell'adozione di tecnologie IA per ottimizzare i processi, migliorare l'efficienza e creare nuovo valore di business.</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
                        <h5 class="font-bold text-blue-600">Eticista dell'IA</h5>
                        <p class="text-sm text-gray-600 mt-2">Un ruolo cruciale che valuta le implicazioni morali e sociali dell'IA, sviluppando linee guida per un uso equo e responsabile.</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
                        <h5 class="font-bold text-blue-600">Analista Sicurezza IA</h5>
                        <p class="text-sm text-gray-600 mt-2">Utilizza tecniche di machine learning per rilevare, prevedere e neutralizzare minacce informatiche in tempo reale, proteggendo i dati sensibili.</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
                        <h5 class="font-bold text-blue-600">Diagnostica Medica Potenziata</h5>
                        <p class="text-sm text-gray-600 mt-2">Medici e ricercatori usano l'IA per analizzare immagini mediche (TAC, raggi X) con una precisione sovrumana, accelerando le diagnosi.</p>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
                        <h5 class="font-bold text-blue-600">Creativo Generativo</h5>
                        <p class="text-sm text-gray-600 mt-2">Artisti, designer e scrittori usano l'IA come partner creativo per generare idee, bozzetti, musiche e testi, espandendo i confini della creatività.</p>
                    </div>
                 </div>
            </div>
        </section>

        <section id="competenze" class="py-16 bg-white rounded-xl shadow-lg">
            <div class="text-center mb-12">
                <h3 class="text-3xl font-bold text-gray-900">Le Competenze del Futuro: Cuore, Cervello e Furbizia</h3>
                <p class="text-gray-600 mt-2 max-w-2xl mx-auto">Mentre l'IA gestisce i dati, il nostro valore risiede nelle capacità unicamente umane. La tecnologia è il copilota, ma noi restiamo al comando della strategia, della creatività e dell'etica.</p>
            </div>
            <div class="grid lg:grid-cols-3 gap-8">
                <div class="lg:col-span-1 space-y-4">
                    <div data-skill="critico" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer transition-all duration-300">
                        <h4 class="font-bold">Pensiero Critico</h4>
                        <p class="text-sm text-gray-600">Analizzare, interpretare e porre le domande giuste.</p>
                    </div>
                    <div data-skill="creativita" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer transition-all duration-300">
                        <h4 class="font-bold">Creatività e Innovazione</h4>
                        <p class="text-sm text-gray-600">Generare idee originali e soluzioni non convenzionali.</p>
                    </div>
                    <div data-skill="agilita" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer transition-all duration-300">
                        <h4 class="font-bold">Agilità di Apprendimento</h4>
                        <p class="text-sm text-gray-600">Imparare rapidamente e adattarsi al cambiamento costante.</p>
                    </div>
                     <div data-skill="empatia" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer transition-all duration-300">
                        <h4 class="font-bold">Empatia e Intelligenza Emotiva</h4>
                        <p class="text-sm text-gray-600">Comprendere gli altri, collaborare e guidare con umanità.</p>
                    </div>
                    <div data-skill="prompt" class="skill-card bg-gray-50 p-4 rounded-lg border-2 border-transparent cursor-pointer transition-all duration-300">
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

        <section id="educazione" class="py-16">
            <div class="text-center mb-12">
                <h3 class="text-3xl font-bold text-gray-900">L'Educazione si Reinventa: Dalla Cattedra al Campo Gioco</h3>
                <p class="text-gray-600 mt-2 max-w-2xl mx-auto">Il vecchio modello basato sulla memorizzazione lascia il posto a un approccio dinamico. L'obiettivo non è più sapere tutto, ma saper imparare, de-imparare e ri-imparare costantemente.</p>
            </div>
            <div class="grid md:grid-cols-2 gap-8">
                <div class="bg-white p-8 rounded-lg shadow-lg fade-in">
                    <h4 class="text-2xl font-bold mb-4 text-red-600">Modello Tradizionale (Obsoleto)</h4>
                    <ul class="space-y-3 text-gray-700 list-disc list-inside">
                        <li>Focus sulla memorizzazione di fatti.</li>
                        <li>Apprendimento "una tantum" per una carriera.</li>
                        <li>Discipline isolate e insegnamento frontale.</li>
                        <li>La conoscenza è un prodotto finito.</li>
                    </ul>
                </div>
                <div class="bg-blue-600 text-white p-8 rounded-lg shadow-lg fade-in">
                    <h4 class="text-2xl font-bold mb-4">Nuovo Paradigma (Adattivo)</h4>
                    <ul class="space-y-3 list-disc list-inside">
                        <li>Focus sull'esplorazione e il pensiero critico.</li>
                        <li>Apprendimento permanente (Lifelong Learning).</li>
                        <li>Approccio transdisciplinare e basato su problemi.</li>
                        <li>La conoscenza è un processo dinamico.</li>
                    </ul>
                </div>
            </div>
        </section>

        <section id="strategie" class="py-16">
            <div class="text-center mb-12">
                <h3 class="text-3xl font-bold text-gray-900">La Tua Guida alla Sopravvivenza (e al Successo)</h3>
                <p class="text-gray-600 mt-2 max-w-2xl mx-auto">Affrontare il cambiamento richiede una strategia. Ecco come individui e organizzazioni possono non solo sopravvivere, ma prosperare affilando costantemente i propri strumenti.</p>
            </div>
            
            <div class="flex justify-center mb-8">
                <div class="bg-gray-200 rounded-full p-1 flex">
                    <button id="btn-individui" class="px-6 py-2 rounded-full text-sm font-semibold transition-colors duration-300 bg-white text-blue-600 shadow">Per gli Individui</button>
                    <button id="btn-organizzazioni" class="px-6 py-2 rounded-full text-sm font-semibold transition-colors duration-300 text-gray-600">Per le Organizzazioni</button>
                </div>
            </div>

            <div id="content-individui" class="grid md:grid-cols-2 gap-8 items-center fade-in">
                <div>
                    <h4 class="text-xl font-bold mb-4">La Tua Cassetta degli Attrezzi Personale</h4>
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
                </div>
                 <div class="bg-white p-8 rounded-lg shadow-lg">
                    <h4 class="font-bold text-lg mb-2">Metafora: Affilare l'Ascia</h4>
                    <p class="text-gray-600">"Se avessi otto ore per abbattere un albero, ne passerei sei ad affilare l'ascia." - Abraham Lincoln. Investire tempo nell'apprendimento (affilare l'ascia) non è una perdita di tempo, ma la strategia più efficace per ottenere risultati migliori con meno sforzo. Il reskilling e l'upskilling sono la tua affilatura quotidiana.</p>
                </div>
            </div>

            <div id="content-organizzazioni" class="hidden grid md:grid-cols-2 gap-8 items-center fade-in">
                 <div>
                    <h4 class="text-xl font-bold mb-4">Costruire una Forza Lavoro a Prova di Futuro</h4>
                    <ul class="space-y-4">
                        <li class="flex items-start">
                            <span class="text-blue-500 mr-3 mt-1">&#10003;</span>
                            <span><strong class="text-gray-900">Crea una Cultura dell'Apprendimento:</strong> Incoraggia e premia la curiosità, la sperimentazione e lo sviluppo continuo. L'apprendimento deve essere parte del DNA aziendale.</span>
                        </li>
                        <li class="flex items-start">
                             <span class="text-blue-500 mr-3 mt-1">&#10003;</span>
                            <span><strong class="text-gray-900">Riprogetta i Ruoli Strategicamente:</strong> Mentre l'IA automatizza i task di routine, ridefinisci le mansioni per valorizzare la creatività, la strategia e l'interazione umana.</span>
                        </li>
                         <li class="flex items-start">
                            <span class="text-blue-500 mr-3 mt-1">&#10003;</span>
                            <span><strong class="text-gray-900">Promuovi la Collaborazione Interfunzionale:</strong> Abbatti i silos. Quando persone di reparti diversi imparano insieme, emergono nuove prospettive e soluzioni innovative.</span>
                        </li>
                         <li class="flex items-start">
                             <span class="text-blue-500 mr-3 mt-1">&#10003;</span>
                            <span><strong class="text-gray-900">Offri Percorsi di Crescita Chiari:</strong> Collega la formazione a reali opportunità di carriera. I dipendenti sono più motivati quando vedono un percorso chiaro per il loro futuro.</span>
                        </li>
                    </ul>
                </div>
                <div class="bg-gray-100 p-8 rounded-lg text-center">
                    <h4 class="font-bold text-lg mb-2">L'Investimento più Intelligente</h4>
                    <p class="text-gray-600">Un'organizzazione che investe nell'adattabilità della propria forza lavoro non sta solo mitigando un rischio, sta costruendo il suo più grande vantaggio competitivo. La tecnologia può essere acquistata, ma una cultura agile e competente deve essere coltivata.</p>
                </div>
            </div>
        </section>

    </main>

    <footer class="bg-gray-800 text-white text-center p-6 mt-16">
        <p>&copy; 2025 Il Futuro è Adattabile. Reinventa te stesso.</p>
    </footer>

<script>
document.addEventListener('DOMContentLoaded', () => {

    const jobMarketCtx = document.getElementById('jobMarketChart').getContext('2d');
    new Chart(jobMarketCtx, {
        type: 'bar',
        data: {
            labels: ['Posti Sostituiti', 'Posti Creati'],
            datasets: [{
                label: 'Milioni di Posti di Lavoro (Stima WEF)',
                data: [85, 97],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.6)', // red-500
                    'rgba(34, 197, 94, 0.6)' // green-500
                ],
                borderColor: [
                    'rgba(239, 68, 68, 1)',
                    'rgba(34, 197, 94, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y} milioni`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Milioni di Posti'
                    }
                }
            }
        }
    });

    const skillDescriptions = {
        critico: {
            title: 'Pensiero Critico e Problem-Solving',
            text: "L'IA fornisce dati, ma il discernimento umano è insostituibile. Questa competenza ti permette di analizzare le informazioni generate dall'IA, identificare bias, porre domande più profonde e risolvere problemi complessi che non hanno una soluzione algoritmica. È l'abilità di dare un senso al rumore."
        },
        creativita: {
            title: 'Creatività e Innovazione',
            text: "Mentre l'IA può ottimizzare e replicare, la vera innovazione nasce dalla creatività umana. È la capacità di connettere idee apparentemente distanti, immaginare il 'what if' e creare qualcosa di genuinamente nuovo. L'IA diventa uno strumento per accelerare il processo creativo, non per sostituirlo."
        },
        agilita: {
            title: 'Agilità di Apprendimento (Learning Agility)',
            text: "In un mondo in costante evoluzione, la capacità di imparare, de-imparare e ri-imparare rapidamente è la competenza fondamentale. Significa essere aperti a nuove esperienze, cercare feedback e adattare il proprio comportamento e le proprie competenze in modo proattivo. Non si tratta di cosa sai, ma di quanto velocemente puoi imparare."
        },
        empatia: {
            title: 'Empatia e Intelligenza Emotiva',
            text: 'Paradossalmente, più la tecnologia avanza, più le abilità umane diventano preziose. L\'empatia permette di comprendere i bisogni dei clienti e dei colleghi, guidare team con umanità e costruire relazioni di fiducia. Sono le soft skills a rendere "dura" e sostenibile l'integrazione tecnologica.'
        },
        prompt: {
            title: 'Prompt Engineering',
            text: "Questa è la nuova frontiera della comunicazione uomo-macchina. È l'arte e la scienza di formulare le giuste domande e istruzioni per guidare i modelli di IA generativa. Padroneggiare questa abilità significa trasformare l'IA da uno strumento generico a un assistente specializzato e incredibilmente potente, capace di produrre esattamente i risultati desiderati."
        }
    };

    const skillCards = document.querySelectorAll('.skill-card');
    const skillDescriptionContainer = document.getElementById('skill-description');

    skillCards.forEach(card => {
        card.addEventListener('click', () => {
            const skillKey = card.dataset.skill;
            
            skillCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');

            const skillInfo = skillDescriptions[skillKey];
            skillDescriptionContainer.innerHTML = `
                <h4 class="text-xl font-bold mb-2 text-blue-700">${skillInfo.title}</h4>
                <p class="text-gray-700">${skillInfo.text}</p>
            `;
        });
    });
    
    if (skillCards.length > 0) {
        skillCards[0].click();
    }


    const btnIndividui = document.getElementById('btn-individui');
    const btnOrganizzazioni = document.getElementById('btn-organizzazioni');
    const contentIndividui = document.getElementById('content-individui');
    const contentOrganizzazioni = document.getElementById('content-organizzazioni');

    btnIndividui.addEventListener('click', () => {
        contentIndividui.classList.remove('hidden');
        contentOrganizzazioni.classList.add('hidden');
        btnIndividui.classList.add('bg-white', 'text-blue-600', 'shadow');
        btnOrganizzazioni.classList.remove('bg-white', 'text-blue-600', 'shadow');
    });

    btnOrganizzazioni.addEventListener('click', () => {
        contentOrganizzazioni.classList.remove('hidden');
        contentIndividui.classList.add('hidden');
        btnOrganizzazioni.classList.add('bg-white', 'text-blue-600', 'shadow');
        btnIndividui.classList.remove('bg-white', 'text-blue-600', 'shadow');
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });

    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });

    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section');

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, { rootMargin: '-30% 0px -70% 0px' });

    sections.forEach(section => {
        sectionObserver.observe(section);
    });

});
</script>

</body>
</html>"""

    print(f"\nTentativo di creare il post (versione HTML): '{post_title}'")
    
    success, result = manager.add_blog_post(
        title=post_title,
        html_content=post_html_content, # Passiamo l'HTML diretto
        author=post_author,
        tags=post_tags,
        status=post_status,
        post_id_slug=post_slug,
        short_description=post_short_description
        # cover_image_url=post_cover_image_url
    )

    if success:
        new_page_id = result
        print(f"\n🎉 Post '{post_title}' (versione HTML) creato con successo nel database 'Articoli del Blog'!")
        print(f"   ID della nuova pagina: {new_page_id}")
        print(f"   Puoi visualizzarlo e modificarlo in Notion.")
        print(f"   Ricorda che è stato creato come '{post_status}'.")
        print(f"   Assicurati di aver aggiunto la proprietà 'HTML Content' (Rich Text) al tuo database Notion.")
    else:
        print(f"\n❌ Fallimento nella creazione del post '{post_title}' (versione HTML).")
        print(f"   Errore: {result}")

if __name__ == "__main__":
    main()