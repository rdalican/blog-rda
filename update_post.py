from app import app, db, Post

post_title = "Adattabilità & IA: Come Ballare con l'Intelligenza Artificiale"
post_content = """
<section id="hero" class="text-center py-16">
    <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">Il Paradosso dell'Adattabilità</h2>
    <p class="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto">Come ballare con l'Intelligenza Artificiale senza perdere il passo (e la testa!). Benvenuti nell'era in cui la nostra capacità di imparare e adattarci è la nostra risorsa più preziosa.</p>
</section>

<section id="mercato" class="py-16">
    <div class="text-center mb-12">
        <h3 class="text-3xl font-bold text-gray-900">Il Nuovo Mercato del Lavoro: Trasformazione, non Apocalisse</h3>
        <div class="mt-8 mb-8">
            <img src="/static/images/ai_workplace_transformation.png" alt="Trasformazione del posto di lavoro nell'era dell'IA" class="mx-auto rounded-lg shadow-lg max-w-3xl w-full">
            <p class="text-sm text-gray-500 mt-2 italic">La collaborazione tra umani e IA sta ridefinendo il futuro del lavoro</p>
        </div>
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

    <div class="mt-8">
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
        <h3 class="text-3xl font-bold text-gray-900">L'Educazione si Reinventa</h3>
        <p class="text-gray-600 mt-2 max-w-2xl mx-auto">Il vecchio modello basato sulla memorizzazione lascia il posto a un approccio dinamico. L'obiettivo non è più sapere tutto, ma saper imparare, de-imparare e ri-imparare costantemente.</p>
    </div>
    
    <div class="grid md:grid-cols-2 gap-8">
        <div class="bg-white p-8 rounded-lg shadow-lg fade-in">
            <h4 class="text-2xl font-bold mb-4 text-red-600">Modello Tradizionale (Obsoleto)</h4>
            <ul class="space-y-3 text-gray-700 list-disc list-inside">
                <li>Focus sulla memorizzazione di fatti</li>
                <li>Apprendimento "una tantum" per una carriera</li>
                <li>Discipline isolate e insegnamento frontale</li>
                <li>La conoscenza è un prodotto finito</li>
            </ul>
        </div>
        <div class="bg-blue-600 text-white p-8 rounded-lg shadow-lg fade-in">
            <h4 class="text-2xl font-bold mb-4">Nuovo Paradigma (Adattivo)</h4>
            <ul class="space-y-3 list-disc list-inside">
                <li>Focus sull'esplorazione e il pensiero critico</li>
                <li>Apprendimento permanente (Lifelong Learning)</li>
                <li>Approccio transdisciplinare e basato su problemi</li>
                <li>La conoscenza è un processo dinamico</li>
            </ul>
        </div>
    </div>
</section>

<section id="conclusione" class="py-16 bg-gray-50">
    <div class="text-center">
        <h3 class="text-3xl font-bold text-gray-900 mb-4">Metafora: Affilare l'Ascia</h3>
        <blockquote class="text-xl text-gray-600 italic mb-4">"Se avessi otto ore per abbattere un albero, ne passerei sei ad affilare l'ascia."</blockquote>
        <p class="text-sm text-gray-500">- Abraham Lincoln</p>
        <p class="mt-4 text-gray-700 max-w-2xl mx-auto">Investire tempo nell'apprendimento (affilare l'ascia) non è una perdita di tempo, ma la strategia più efficace per ottenere risultati migliori con meno sforzo. Il reskilling e l'upskilling sono la tua affilatura quotidiana.</p>
    </div>
</section>

<script>
document.addEventListener('DOMContentLoaded', () => {
    // Inizializzazione del grafico
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

    // Gestione delle skill card
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
            text: 'Paradossalmente, più la tecnologia avanza, più le abilità umane diventano preziose. L\\'empatia permette di comprendere i bisogni dei clienti e dei colleghi, guidare team con umanità e costruire relazioni di fiducia. Sono le soft skills a rendere "dura" e sostenibile l\\'integrazione tecnologica.'
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

    // Animazioni di fade-in
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
});
</script>
"""

with app.app_context():
    # Delete existing posts
    Post.query.delete()
    
    # Create new post
    new_post = Post(title=post_title, content=post_content)
    db.session.add(new_post)
    db.session.commit()
    print("Post created successfully!")
