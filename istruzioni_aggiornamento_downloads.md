# Istruzioni per l'aggiornamento della pagina "Software Gratuito"

## Obiettivo
Aggiungere una sezione "Tutorial Video" alla pagina "Software Gratuito" (downloads.html) con i 9 video tutorial caricati su YouTube.

## Posizione dell'inserimento
Inserire la nuova sezione dopo il video tutorial introduttivo (riga 17) e prima della sezione di download (riga 19).

## Codice HTML da inserire

```html
<div class="max-w-5xl mx-auto bg-white rounded-lg shadow-lg p-8 mb-12">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">Tutorial Video</h2>
    <p class="text-gray-600 mb-6">
        Guarda i nostri video tutorial per imparare a utilizzare tutte le funzionalità del software "Sistematica Commerciale".
    </p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Video 1 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/6zbvPxwj3JE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Capitolo 1: Strategia e Tattica</h3>
                <p class="text-gray-600 text-sm">Impara le basi della strategia commerciale e le tattiche per avere successo nelle vendite.</p>
            </div>
        </div>
        
        <!-- Video 2 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/wG6o7lzpz-4" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Capitolo 2: I 4 tipi di compratore</h3>
                <p class="text-gray-600 text-sm">Scopri come identificare e approcciare i diversi tipi di clienti.</p>
            </div>
        </div>
        
        <!-- Video 3 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/JNFBqYcSKCU" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Capitolo 3: La Chiave per Ogni Vendita</h3>
                <p class="text-gray-600 text-sm">Scopri l'elemento fondamentale che deve essere presente in ogni processo di vendita.</p>
            </div>
        </div>
        
        <!-- Video 4 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/sveskpAVSxs" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Capitolo 4: I Modi del Compratore</h3>
                <p class="text-gray-600 text-sm">Impara a riconoscere i diversi modi in cui i clienti prendono decisioni di acquisto.</p>
            </div>
        </div>
        
        <!-- Video 5 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/1MxJUJjrrKo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Capitolo 5: L'arte di Vincere Davvero</h3>
                <p class="text-gray-600 text-sm">Scopri come creare valore reale per il cliente e costruire relazioni durature.</p>
            </div>
        </div>
        
        <!-- Video 6 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/61V8Fjiv6wg" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Capitolo 6: Risultati e Vincite - L'Anatomia di una Vendita</h3>
                <p class="text-gray-600 text-sm">Analizza le componenti fondamentali di una vendita di successo.</p>
            </div>
        </div>
        
        <!-- Video 7 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/S9CNlgsE19A" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Capitolo 7: L'Imbuto di Vendita</h3>
                <p class="text-gray-600 text-sm">Impara a gestire il processo di vendita dall'inizio alla chiusura.</p>
            </div>
        </div>
        
        <!-- Video 8 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/baury4O8uiw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Capitolo 8: Il Cliente Ideale</h3>
                <p class="text-gray-600 text-sm">Scopri come identificare e coltivare relazioni con i clienti più redditizi.</p>
            </div>
        </div>
        
        <!-- Video 9 -->
        <div class="bg-gray-50 rounded-lg shadow-md overflow-hidden">
            <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
                <iframe src="https://www.youtube.com/embed/hzlONNsztow" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border-radius: 8px;"></iframe>
            </div>
            <div class="p-4">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Premessa: Riscoprire il Venditore</h3>
                <p class="text-gray-600 text-sm">Introduzione al mindset del venditore professionista.</p>
            </div>
        </div>
    </div>
</div>
```

## Verifica
Dopo aver inserito il codice, aprire la pagina "Software Gratuito" nel browser e verificare che:
1. La sezione "Tutorial Video" sia visibile dopo il video introduttivo.
2. Tutti e 9 i video vengano visualizzati correttamente nella griglia.
3. I video si riproducano correttamente quando si clicca su di essi.
4. La pagina sia responsive e i video si adattino correttamente alle diverse dimensioni dello schermo.